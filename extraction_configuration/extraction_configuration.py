import yaml
from typing import Any


class ExtractionConfiguration:
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
        return self._yaml_configuration.get(key)

    def get_extractor_module_name(self) -> Any:
        return self._yaml_configuration.get("extractor")[0].get("module_name")

    def get_extractor_class_name(self) -> Any:
        return self._yaml_configuration.get("extractor")[0].get("class_name")
