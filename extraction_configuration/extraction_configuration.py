import importlib
from extractors.extractor import Extractor


class ExtractionConfiguration:
    def __init__(
        self,
        yaml_configuration: [str],
    ):
        self._yaml_configuration = yaml_configuration

    def get_field(self, key: str):
        return self._yaml_configuration.get(key)

    def get_extractor_module_name(self):
        return self._yaml_configuration.get("extractor")[0].get("module_name")

    def get_extractor_class_name(self):
        return self._yaml_configuration.get("extractor")[0].get("class_name")
