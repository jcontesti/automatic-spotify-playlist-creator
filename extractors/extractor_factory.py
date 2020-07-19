from extractors.extractor import Extractor
from extractors.scrapy_extractor import ScrapyExtractor
import importlib


class ExtractorFactory:
    @staticmethod
    def get_extractor(
            module_name: str,
            class_name: str,
    ) -> Extractor:
        module = importlib.import_module(module_name)
        extractor = getattr(module, class_name)

        if issubclass(extractor, ScrapyExtractor):
            return ScrapyExtractor(module_name, class_name, module, extractor)
