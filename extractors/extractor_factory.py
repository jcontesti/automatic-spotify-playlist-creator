from extractors.extractor import Extractor
from extractors.scrapy_extractor import ScrapyExtractor
from types import ModuleType
from typing import Any, Optional
import importlib


class ExtractorFactory:

    @staticmethod
    def get_extractor(
            module_name: str,
            class_name: str,
    ) -> Optional[Extractor]:
        module: ModuleType = importlib.import_module(module_name)
        extractor: Any = getattr(module, class_name)

        if issubclass(extractor, ScrapyExtractor):
            return ScrapyExtractor(module_name, class_name, module, extractor)
        else:
            return None
