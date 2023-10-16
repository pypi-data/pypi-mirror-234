import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import timedelta, datetime
from typing import Optional, Any, List, Callable

import aiohttp
from aiohttp import ClientSession, ClientResponse
from solidlab_perftest_common import status
from solidlab_perftest_common.agent import (
    AgentCommand,
    AgentCommandResult,
    AgentCommandResultStatus,
    Agent,
    AgentCommandFull,
)
from solidlab_perftest_common.content_types import SolidLabContentType
from solidlab_perftest_common.pagination import Page
from solidlab_perftest_common.util import datetime_now, dump_rfc3339

from solidlab_perftest_agent.config import Config


class ApiError(Exception):
    @classmethod
    async def make(
        cls,
        message: str,
        response: Optional[ClientResponse],
        *,
        response_body: Optional[Any] = None,
    ) -> "ApiError":
        if response and not response_body:
            try:
                response_body = (
                    await response.text()
                    if response.content_type == "text/plain"
                    else await response.json()
                )
            except:
                pass  # ignore error fetching body of response
        return ApiError(message, response, response_body=response_body)

    def __init__(
        self,
        message: str,
        response: Optional[ClientResponse],
        *,
        response_body: Optional[Any] = None,
    ):
        super().__init__()
        self.message = message
        self.response = response
        self.response_body = response_body

    def __str__(self) -> str:
        if self.response:
            return f"ApiError({self.message}, status={self.response.status}, body={self.response_body})"
        else:
            return f"ApiError({self.message})"


# class SessionRetryWrapper:
#     def __int__(self, session_maker: Callable[[], ClientSession]):
#         self.session_maker = session_maker
#
#     @asynccontextmanager
#     def put(self, *args, **kwargs):
#         tries = 0
#         while tries < 5:
#             tries += 1
#             async with self.session_maker() as session:
#                 async with session.put(*args, **kwargs) as response:
#                     if response.status in (
#                         status.HTTP_502_BAD_GATEWAY,
#                         status.HTTP_503_SERVICE_UNAVAILABLE,
#                         status.HTTP_504_GATEWAY_TIMEOUT,
#                     ):
#                         logging.warning(
#                             f"Got response {response.status} {response.reason} "
#                             f"-> (this was attempt {tries}) will wait and retry"
#                         )
#                         await asyncio.sleep(1)
#                         continue  # retry
#                     yield response
#
#     @asynccontextmanager
#     def get(self, *args, **kwargs):
#         tries = 0
#         while tries < 5:
#             tries += 1
#             async with self.session_maker() as session:
#                 async with session.get(*args, **kwargs) as response:
#                     if response.status in (
#                         status.HTTP_502_BAD_GATEWAY,
#                         status.HTTP_503_SERVICE_UNAVAILABLE,
#                         status.HTTP_504_GATEWAY_TIMEOUT,
#                     ):
#                         logging.warning(
#                             f"Got response {response.status} {response.reason} "
#                             f"-> (this was attempt {tries}) will wait and retry"
#                         )
#                         await asyncio.sleep(1)
#                         continue  # retry
#                     yield response


class Api:
    def __init__(self, config: Config):
        self.config = config
        self.agent_url = f"{self.config.api_endpoint}testenv/{self.config.test_env_id}/agent/{self.config.machine_id}"
        self.session_maker: Callable[[], ClientSession] = lambda: aiohttp.ClientSession(
            # auth=BasicAuth(
            #     login=get_settings().GITHUB_USER, password=get_settings().GITHUB_PASS
            # )
            headers={
                "Solidlab-PerfTest-Auth": config.auth_token,
                "Accept": "application/json",
            },
        )

    async def agent_hello(self):
        async with self.session_maker() as session:
            async with session.put(
                self.agent_url,
                data=Agent(
                    testenv_id=self.config.test_env_id,
                    machine_id=self.config.machine_id,
                    last_active=datetime_now(),
                    active=True,
                ).json(),
                headers={"Content-Type": SolidLabContentType.AGENT_STATUS.value},
            ) as response:
                if not response.ok:
                    raise await ApiError.make("Failed to say hello", response)

    async def agent_goodbye(self):
        async with self.session_maker() as session:
            async with session.put(
                self.agent_url,
                data=Agent(
                    testenv_id=self.config.test_env_id,
                    machine_id=self.config.machine_id,
                    last_active=datetime_now(),
                    active=False,
                ).json(),
                headers={"Content-Type": SolidLabContentType.AGENT_STATUS.value},
            ) as response:
                if not response.ok:
                    raise await ApiError.make("Failed to say goodbye", response)

    async def request_commands(self) -> List[AgentCommand]:
        start_request = datetime_now()
        res_len = 0
        try:
            url = f"{self.agent_url}/command"
            async with self.session_maker() as session:
                async with session.get(
                    url,
                    headers={"Accept": SolidLabContentType.AGENT_COMMAND.value},
                    params={"finished": "false", "wait_s": 5.0},
                ) as response:
                    if not response.ok:
                        raise await ApiError.make("Failed to fetch command", response)
                    if response.status == status.HTTP_204_NO_CONTENT:
                        return []
                    resp_obj = await response.json()
                    # This returns a dict version of Page[AgentCommandFull]
                    if not resp_obj:
                        return []
                    if not isinstance(resp_obj, dict) or "total" not in resp_obj:
                        raise await ApiError.make(
                            f"Got unexpected response to {url}",
                            response,
                            response_body=resp_obj,
                        )
                    bound_page_class = Page[AgentCommandFull]
                    try:
                        page = bound_page_class.parse_obj(resp_obj)
                    except:
                        raise await ApiError.make(
                            f"Got unexpected response to {url}",
                            response,
                            response_body=resp_obj,
                        )
                    # TODO: handle that this only returns first commands of many, if page.total > page.size
                    #       (but that can probably be ignored: new commands will just be requested later)
                    res_len = len(page.items)
                    return [AgentCommand.parse_obj(ac) for ac in page.items]
            return []
        finally:
            # make sure that if no commands are found, this call takes long enough
            if res_len == 0:
                end_request = datetime_now()
                req_dur = end_request - start_request
                min_duration = timedelta(seconds=2)
                if req_dur < min_duration:
                    sleep_needed_s = (min_duration - req_dur).total_seconds()
                    logging.warning(
                        f"Need to wait a bit after getting no commands: {sleep_needed_s}s"
                    )
                    await asyncio.sleep(sleep_needed_s)

    async def report_command_start(
        self, command: AgentCommand, started: Optional[datetime] = None
    ) -> None:
        started = started if started is not None else datetime_now()
        url = f"{self.agent_url}/command/{command.id}/started"
        async with self.session_maker() as session:
            async with session.put(
                url,
                data=dump_rfc3339(started, no_milliseconds=False),
            ) as response:
                if not response.ok:
                    raise await ApiError.make(
                        "Failed to report command start", response
                    )

    # async def report_command_status(
    #     self,
    #     command: AgentCommand,
    #     status: AgentCommandResultStatus,
    #     return_value: Optional[int] = None,
    #     error_msg: Optional[str] = None,
    #     trace: Optional[str] = None,
    #     debug_msg: Optional[str] = None,
    #     stdout: Optional[str] = None,
    #     stderr: Optional[str] = None,
    # ) -> None:
    #     await self.report_command_result(
    #         command,
    #         AgentCommandResult(
    #             command_id=command.id,
    #             status=status,
    #             return_value=return_value,
    #             error_msg=error_msg,
    #             trace=trace,
    #             debug_msg=debug_msg,
    #             stdout=stdout,
    #             stderr=stderr,
    #             started=???,
    #             stopped=datetime_now(),
    #         ),
    #     )

    async def report_command_result(
        self, command: AgentCommand, res: AgentCommandResult
    ) -> None:
        url = f"{self.agent_url}/command/{command.id}/result"
        async with self.session_maker() as session:
            async with session.put(
                url,
                data=res.json(),
                headers={
                    "Content-Type": SolidLabContentType.AGENT_COMMAND_RESULT.value
                },
            ) as response:
                if not response.ok:
                    if response.status == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE:
                        # retry with less data
                        def reduce_len(v: Optional[str]) -> Optional[str]:
                            if not v:
                                return v
                            if len(v) < 4096:
                                return v
                            return f"DROPPED: TOO LARGE ({len(v)} byte)"

                        async with session.put(
                            url,
                            data=AgentCommandResult(
                                command_id=res.command_id,
                                status=res.status,
                                return_value=res.return_value,
                                error_msg=reduce_len(res.error_msg),
                                trace=reduce_len(res.trace),
                                debug_msg=reduce_len(res.debug_msg),
                                stdout=reduce_len(res.stdout),
                                stderr=reduce_len(res.stderr),
                                started=res.started,
                                stopped=res.stopped,
                            ).json(),
                            headers={
                                "Content-Type": SolidLabContentType.AGENT_COMMAND_RESULT.value
                            },
                        ) as response:
                            if not response.ok:
                                raise await ApiError.make(
                                    "Failed to report command result on 2nd attempt",
                                    response,
                                )
                    else:
                        raise await ApiError.make(
                            "Failed to report command result", response
                        )
