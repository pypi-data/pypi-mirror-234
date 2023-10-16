from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    api_endpoint: str
    machine_id: str
    test_env_id: int
    auth_token: str
    # Below: Config depending on the test environment this agent is running on.
    #        Probably fixed values in the ESpec that sets up the test environment.
    css_config_file: Optional[str]
    perfstat_env_file: Optional[str]
    css_host: Optional[str]
    css_port: Optional[str]
