"""Class to load and return the configuration of a playlist extraction."""
from typing import Any

import yaml


class ExtractionConfiguration:
    """Class to load and return the configuration of a playlist extraction."""

    def __init__(
        self,
        configuration_file_path: str,
    ) -> None:
        self._yaml_configuration: Any = (
                self._read_yaml(configuration_file_path)
        )

    @staticmethod
    def _read_yaml(
            yaml_file: str
    ) -> Any:
        with open(yaml_file, "r") as stream:
            return yaml.safe_load(stream)

    def get_field(self, key: str) -> Any:
        """Get any field in the configuration."""
        return self._yaml_configuration.get(key)

    def get_extractor_module_name(self) -> Any:
        """Get the module name of the extractor."""
        return self._yaml_configuration.get("extractor")[0].get("module_name")

    def get_extractor_class_name(self) -> Any:
        """Get the class name of the extractor."""
        return self._yaml_configuration.get("extractor")[0].get("class_name")
