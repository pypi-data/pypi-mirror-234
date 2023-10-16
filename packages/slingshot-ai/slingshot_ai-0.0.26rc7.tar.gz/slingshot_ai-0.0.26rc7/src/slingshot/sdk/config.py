from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .. import schemas
from .config_utils import BaseJSONSettings

"""
We have three types of settings:
- ClientSettings just state defaults for where to store stuff on the client's machine
- LocalConfig is the local config file for a specific project. This may include the project id or anything cached from
recent API calls.
- GlobalConfig is the global config file for the user. This may include auth info, etc.
"""


def _find_project_folder() -> Path:
    # ENG-1961: We used to look for a .slingshot directory in either the current directory or any ancestor directory.
    # This was removed as it led to confusion where multiple slingshot projects were nested inside each other
    # (no purpose or by accident). We now always use the current working directory as the project directory. To revert
    # this behavior, look for the PR tagged ENG-1961 and undo.
    return Path(os.getcwd()) / ".slingshot"


class ClientSettings(BaseSettings):
    """Settings for the client"""

    project_config_folder: Path = _find_project_folder()
    global_config_folder: Path = Path.home() / ".slingshot_config"
    slingshot_config_filename: str = "slingshot.yaml"
    slingshot_config_path: Path = project_config_folder.parent / slingshot_config_filename

    # These are set if you're running within a slingshot app
    slingshot_component_type: Optional[schemas.ComponentType] = None
    slingshot_instance_id: Optional[str] = None
    slingshot_spec_id: Optional[str] = None

    @property
    def is_in_app(self) -> bool:
        return self.slingshot_component_type is not None


client_settings = ClientSettings()


class GlobalConfig(BaseJSONSettings):
    slingshot_local_url: str = "http://localhost:8002"
    slingshot_dev_url: str = "https://dev.slingshot.xyz"
    slingshot_prod_url: str = "https://app.slingshot.xyz"
    slingshot_backend_url: str = slingshot_prod_url  # rstrip("/") is called on this
    hasura_admin_secret: Optional[str] = None
    auth_token: Optional[schemas.AuthTokenUnion] = None
    check_for_updates_interval: float = 60 * 60 * 1  # 1 hour
    last_checked_for_updates: Optional[float] = None
    # TODO: We have magic that uses config_file at runtime even though it's not statically typed, clean this up
    model_config = SettingsConfigDict(config_file=client_settings.global_config_folder / "config.json")  # type: ignore

    @classmethod
    @field_validator("slingshot_backend_url")
    def slingshot_backend_url_strip_slash(cls, v: str) -> str:
        # If a backend is set in global_config, use that instead of the default or env var
        v = v.rstrip("/")
        return v


class ProjectConfig(BaseJSONSettings):
    project_id: Optional[str] = None
    last_pushed_manifest: Optional[dict[str, Any]] = None
    # TODO: We have magic that uses config_file at runtime even though it's not statically typed, clean this up
    model_config = SettingsConfigDict(config_file=client_settings.project_config_folder / "config.json")  # type: ignore


global_config = GlobalConfig()
project_config = ProjectConfig()
