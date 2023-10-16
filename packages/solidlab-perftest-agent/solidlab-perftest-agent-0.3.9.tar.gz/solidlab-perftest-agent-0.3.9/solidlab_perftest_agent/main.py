import asyncio
import logging
import signal
import sys
import traceback
from textwrap import dedent
from typing import List

import aiofiles
import aiohttp
from solidlab_perftest_common.agent import (
    AgentCommandResultStatus,
    AgentCommand,
    AgentCommandType,
    AgentCommandResult,
)
from solidlab_perftest_common.util import call_external_command_async, datetime_now

from solidlab_perftest_agent.api_calls import Api, ApiError
from solidlab_perftest_agent.config import Config

main_loop_active = True


class CommandExecutor:
    # This is a class instead of a method, because to handle timeout, we need to have access to the partial result.
    def __init__(self, command: AgentCommand, config: Config, api: Api):
        self.command = command
        self.config = config
        self.api = api
        self.stdout_s = None
        self.stderr_s = None
        self.err_s = None
        self.debug_s = None
        self.trace = None
        self.return_value = None
        self.called = False
        self.started = None
        self.stopped = None

        # It is handy to make the config available to executed command via the environment
        self.env = {
            "PERFTEST_AGENT_API_ENDPOINT": str(config.api_endpoint),
            "PERFTEST_AGENT_MACHINE_ID": str(config.machine_id),
            "PERFTEST_AGENT_TEST_ENV_ID": str(config.test_env_id),
            "PERFTEST_AGENT_AUTH_TOKEN": str(config.auth_token),
        }
        if self.config.css_config_file:
            self.env["PERFTEST_AGENT_CSS_CONFIG_FILE"] = str(
                self.config.css_config_file
            )
        if self.config.perfstat_env_file:
            self.env["PERFTEST_AGENT_PERFSTAT_ENV_FILE"] = str(
                self.config.perfstat_env_file
            )
        if self.config.css_host:
            self.env["PERFTEST_AGENT_CSS_HOST"] = str(self.config.css_host)
        if self.config.css_port:
            self.env["PERFTEST_AGENT_CSS_PORT"] = str(self.config.css_port)

    def _stdout_handler(self, msg: str):
        self.stdout_s += msg + "\n"

    def _stderr_handler(self, msg: str):
        self.stderr_s += msg + "\n"

    def _error_log_handler(self, msg: str):
        self.err_s += msg + "\n"

    def _debug_log_handler(self, msg: str):
        self.debug_s += msg + "\n"

    def get_status(self, status: AgentCommandResultStatus) -> AgentCommandResult:
        return AgentCommandResult(
            command_id=self.command.id,
            status=status,
            return_value=self.return_value,
            error_msg=self.err_s if self.err_s else None,
            trace=None,
            debug_msg=self.debug_s if self.debug_s else None,
            stdout=self.stdout_s if self.stdout_s else None,
            stderr=self.stderr_s if self.stderr_s else None,
            started=self.started or self.stopped or datetime_now(),
            stopped=self.stopped or datetime_now(),
        )

    async def execute(self) -> bool:
        assert not self.called
        self.called = True
        try:
            if self.command.type == AgentCommandType.WRITE_FILE:
                assert isinstance(self.command.data, List)
                assert self.command.data
                assert len(self.command.data) == 2
                file_name = self.command.data[0]
                file_content = self.command.data[1]
                assert isinstance(file_name, str)
                assert isinstance(file_content, str)
                if file_name == "__CSS_CONFIG__":
                    file_name = self.config.css_config_file
                if file_name == "__PERFSTAT_ENVS__":
                    file_name = self.config.perfstat_env_file

                self.started = datetime_now()
                async with aiofiles.open(file_name, mode="w") as f:
                    bytes_written = await f.write(file_content)
                    self.debug_s = f"wrote {bytes_written} bytes to {file_name}"
                self.stopped = datetime_now()

                await self.api.report_command_result(
                    self.command, self.get_status(AgentCommandResultStatus.SUCCESS)
                )
                return True

            self.stdout_s = ""
            self.stderr_s = ""
            self.err_s = ""
            self.debug_s = ""

            if self.command.type == AgentCommandType.STOP_SERVICE:
                assert isinstance(self.command.data, str)
                assert self.command.data
                self.started = datetime_now()
                self.return_value = await call_external_command_async(
                    command=["/usr/bin/systemctl", "stop", self.command.data],
                    timeout_s=self.command.timeout_s,
                    stdout_handler=self._stdout_handler,
                    stderr_handler=self._stderr_handler,
                    debug_log_handler=self._debug_log_handler,
                    error_log_handler=self._error_log_handler,
                )
                self.stopped = datetime_now()
            elif self.command.type == AgentCommandType.START_SERVICE:
                assert isinstance(self.command.data, str)
                assert self.command.data
                self.started = datetime_now()
                self.return_value = await call_external_command_async(
                    command=["/usr/bin/systemctl", "restart", self.command.data],
                    timeout_s=self.command.timeout_s,
                    stdout_handler=self._stdout_handler,
                    stderr_handler=self._stderr_handler,
                    debug_log_handler=self._debug_log_handler,
                    error_log_handler=self._error_log_handler,
                )
                self.stopped = datetime_now()
            elif self.command.type == AgentCommandType.EXEC_BASH:
                assert isinstance(self.command.data, list)
                assert self.command.data
                assert all(isinstance(c, str) for c in self.command.data)
                self.started = datetime_now()
                self.return_value = await call_external_command_async(
                    command=self.command.data,
                    timeout_s=self.command.timeout_s,
                    stdout_handler=self._stdout_handler,
                    stderr_handler=self._stderr_handler,
                    debug_log_handler=self._debug_log_handler,
                    error_log_handler=self._error_log_handler,
                    env=self.env,
                )
                self.stopped = datetime_now()
            else:
                raise ValueError(f"Unsupported AgentCommandType: {self.command.type}")

            status = (
                AgentCommandResultStatus.SUCCESS
                if self.return_value == 0
                else AgentCommandResultStatus.FAILURE
            )
            duration_s = (self.stopped - self.started).total_seconds()
            self.debug_s += (
                f"Command stopped after {duration_s}s. status={status.name}\n"
            )

            await self.api.report_command_result(
                self.command,
                self.get_status(status),
            )
            return True
        except TimeoutError as e:
            self.stopped = datetime_now()
            self.trace = None
            status = AgentCommandResultStatus.TIMEOUT
            duration_s = (self.stopped - self.started).total_seconds()
            self.debug_s += f"Command raised TimeoutError after {duration_s}s. status={status.name}\n"
            try:
                await self.api.report_command_result(
                    self.command, self.get_status(status)
                )
            except ApiError:
                logging.exception(
                    "Failed to submit command status on timeout. Probably conflict. Will ignore."
                )
            return False
        except Exception as e:
            self.stopped = datetime_now()
            self.trace = "".join(traceback.format_exception(None, e, e.__traceback__))
            status = AgentCommandResultStatus.FAILURE
            duration_s = (self.stopped - self.started).total_seconds()
            self.debug_s += (
                f"Command raised Exception after {duration_s}s. status={status.name}\n"
            )
            try:
                await self.api.report_command_result(
                    self.command, self.get_status(status)
                )
            except ApiError:
                logging.exception(
                    "Failed to submit command status on failure. Probably conflict. Will ignore."
                )
            return False


async def hello_loop(api: Api):
    # Keep saying hello periodically.
    while True:
        await asyncio.sleep(30)
        logging.info(f"Agent will say Hello")
        await api.agent_hello()


async def async_main(config: Config) -> int:
    api = Api(config)
    logging.info(f"Agent will say Hello")
    await api.agent_hello()
    logging.info(f"Agent said Hello")

    hello_task = asyncio.create_task(hello_loop(api))

    try:
        while main_loop_active:
            try:
                commands = await api.request_commands()
            except:
                logging.error(
                    f"Failed to request commands. Will wait 5 seconds and try again."
                )
                await asyncio.sleep(5)
                continue

            logging.debug(f"Request commands returned {len(commands)} commands")
            if commands:
                for command in commands:
                    logging.info(f"Executing command: {command}")
                    await api.report_command_start(command)
                    command_executor = CommandExecutor(command, config, api)
                    try:
                        # timeout + 1 to give internal timeout check chance to work first
                        command_success = await asyncio.wait_for(
                            command_executor.execute(), timeout=command.timeout_s + 1
                        )
                        if not command_success:
                            # give server time to digest command failure info
                            logging.error(
                                f"Failed to execute command: command reported failure"
                            )
                            await asyncio.sleep(0.5)
                            # Forget the current list of commands
                            # The server will (send them again)/(not remove them) if they don't need to be cancelled.
                            break
                    except asyncio.TimeoutError:
                        logging.info(f"Failed to execute command: command timed out")
                        status = AgentCommandResultStatus.TIMEOUT
                        if not command_executor.stopped:
                            command_executor.stopped = datetime_now()
                        duration_s = (
                            command_executor.stopped - command_executor.started
                        ).total_seconds()
                        command_executor.debug_s += f"Command cancelled due to timeout after {duration_s}s. status={status.name}\n"
                        try:
                            await api.report_command_result(
                                command,
                                command_executor.get_status(status),
                            )
                        except ApiError:
                            # This can fail because there is a result already.
                            # That's OK, whatever that result is, it has precedence over this timeout.
                            logging.exception(
                                "Ignoring failure to report command result.)"
                            )
                        # give server time to digest this info
                        await asyncio.sleep(0.5)
                        # Forget the current list of commands
                        # The server will (send them again)/(not remove them) if they don't need to be cancelled.
                        break
    finally:
        hello_task.cancel()
        await asyncio.sleep(0.5)  # wait for cancelled
        logging.info(f"Agent will say Goodbye")
        await api.agent_goodbye()
        logging.info(f"Agent said Goodbye")

    return 0


def main() -> int:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # agent is not meant to be called manually, so it has very strict parameters
    show_help = True
    config = None
    if len(sys.argv) == 9:
        api_endpoint = sys.argv[1].strip()
        show_help = not api_endpoint.startswith("http")
        if show_help:
            print("ERROR: Bad <api_endpoint>", file=sys.stderr)
        assert api_endpoint.startswith("http")
        assert "/perftest/" not in api_endpoint
        assert "/artifact/" not in api_endpoint
        if not api_endpoint.endswith("/"):
            api_endpoint += "/"

        machine_id = sys.argv[2].strip()
        if not machine_id:
            print("ERROR: Missing <machine_id>", file=sys.stderr)
        show_help = show_help or not machine_id

        try:
            test_env_id = int(sys.argv[3].strip())
            show_help = show_help or not test_env_id
            if not test_env_id:
                print("ERROR: Missing <test_env_id>", file=sys.stderr)
        except ValueError:
            show_help = True
            test_env_id = None
            print("ERROR: Bad <test_env_id>", file=sys.stderr)

        auth_token = sys.argv[4].strip()
        show_help = show_help or not auth_token
        if not auth_token:
            print("ERROR: Missing <auth_token>", file=sys.stderr)

        css_config_file = (
            sys.argv[5].strip()
            if sys.argv[5].strip() and sys.argv[5].strip().lower() != "none"
            else None
        )
        perfstat_env_file = (
            sys.argv[6].strip()
            if sys.argv[6].strip() and sys.argv[6].strip().lower() != "none"
            else None
        )
        css_host = (
            sys.argv[7].strip()
            if sys.argv[7].strip() and sys.argv[7].strip().lower() != "none"
            else None
        )
        if sys.argv[8].strip() and sys.argv[8].strip().lower() != "none":
            try:
                css_port = int(sys.argv[8].strip())
            except:
                print(f"Invalid css_port arg: {sys.argv[8]!r}")
                raise

        config = Config(
            api_endpoint=api_endpoint,
            machine_id=machine_id,
            test_env_id=test_env_id,
            auth_token=auth_token,
            css_config_file=css_config_file,
            perfstat_env_file=perfstat_env_file,
            css_host=css_host,
            css_port=css_port,
        )

    if show_help:
        print(
            f"""Usage: {sys.argv[0]} <api_endpoint> <machine_id> <test_env_id> <auth_token> <css_config_file> <perfstat_env_file> <css_host> <css_port>
   api_endpoint: the URL of the solidlab-perftest-server API endpoint (example: 'https://example.com/perftest_api/v1/')
   machine_id: the ID of the machine this agent runs on (str)
   test_env_id: the ID of the TestEnv (int)
   auth_token: the auth token needed to POST to api_endpoint (str)
   css_config_file: the full path of the css config file (or "none" if not on the server itself) (str)
   perfstat_env_file: the full path of the perfstat env file (or "none" if there is none) (str)
   css_host: the hostname on which the css can be reached (or "none" on css server itself) (str)
   css_port: the port on which the css can be reached (or "none" on css server itself) (str)
        """,
            file=sys.stderr,
        )
        return 1

    # noinspection PyUnusedLocal
    def signal_handler(sig, frame):
        print(f"{signal.Signals(sig).name} received. Will finishing work.")
        # Stop agent gracefully
        global main_loop_active
        main_loop_active = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    retval = asyncio.run(async_main(config))

    return retval


if __name__ == "__main__":
    sys.exit(main())
