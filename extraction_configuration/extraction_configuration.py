import importlib
from extractors.extractor import Extractor


class ExtractionConfiguration:
    def __init__(
        self,
        yaml_configuration: [str],
    ):
        self._yaml_configuration = yaml_configuration
        self._extractor = self._load_extractor()

    def _load_extractor(self) -> Extractor:
        module_name = self._yaml_configuration.get("extractor").get("module_name")
        class_name = self._yaml_configuration.get("extractor").get("class_name")

        spider_module = importlib.import_module(module_name)
        return getattr(spider_module, class_name)

    def get_field(self, key: str):
        return self._yaml_configuration.get(key)

    def get_extractor(self):
        return self._extractor
