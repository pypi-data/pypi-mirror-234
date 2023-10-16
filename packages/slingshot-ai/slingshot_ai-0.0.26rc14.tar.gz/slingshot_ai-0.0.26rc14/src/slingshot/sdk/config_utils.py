from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Type

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """
    Source for settings that are saved to, and loaded from a JSON file, with the path specified in the "config_file"
    defined in the model config for the settings class.

    See https://docs.pydantic.dev/latest/usage/pydantic_settings/#adding-sources for more context.
    """

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        settings_json_file = self.config.get('config_file')
        assert isinstance(settings_json_file, Path), f"settings_json_file must be a Path, got {settings_json_file}"
        if not settings_json_file.exists():
            return None, field_name, False

        try:
            file_content_json = json.loads(settings_json_file.read_text())
        except json.JSONDecodeError as e:
            return None, field_name, False

        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                d[field_key] = field_value

        return d


class BaseJSONSettings(BaseSettings):
    """
    Base class for settings that are saved to a JSON file.
    Whenever an attribute is set, the settings are saved to the JSON file.
    """

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, JsonConfigSettingsSource(settings_cls), env_settings, file_secret_settings)

    def __setattr__(self, key: str, value: Any) -> None:
        if not hasattr(self, key):
            raise AttributeError(f"Cannot set attribute {key} on {self}")
        super().__setattr__(key, value)
        self._save()

    def _save(self) -> None:
        settings_json_file = self.model_config.get('config_file')
        assert isinstance(settings_json_file, Path), f"settings_json_file must be a Path, got {settings_json_file}"
        os.makedirs(settings_json_file.parent, exist_ok=True)
        with open(settings_json_file, "w") as f:
            model_dict = self.model_dump(warnings=False)  # Ignore warnings about dict vs ProjectManifest
            json.dump(model_dict, f, indent=4)
