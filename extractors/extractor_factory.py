"""Extractor objects factory class."""
import importlib
from types import ModuleType
from typing import Any, Optional

from extractors.extractor import Extractor
from extractors.scrapy_extractor import ScrapyExtractor


class ExtractorFactory:
    """Extractor objects factory class."""

    @staticmethod
    def get_extractor(
            module_name: str,
            class_name: str,
    ) -> Optional[Extractor]:  # pylint: disable=unsubscriptable-object
        """Return the extractor that will load the playlist."""
        module: ModuleType = importlib.import_module(module_name)
        extractor: Any = getattr(module, class_name)

        # pylint: disable=unsubscriptable-object
        loaded_extractor: Optional[Extractor] = None

        if issubclass(extractor, ScrapyExtractor):
            loaded_extractor = ScrapyExtractor(
                module_name,
                class_name,
                module,
                extractor
            )

        return loaded_extractor
