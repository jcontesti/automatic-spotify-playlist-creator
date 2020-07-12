from abc import ABC, abstractmethod
from extracted_data.extracted_playlist import ExtractedPlaylist


class Extractor(ABC):

    @abstractmethod
    def add_extractor(self, module_name: str, class_name: str):
        pass

    @abstractmethod
    def execute_extractors(self):
        pass

    @abstractmethod
    def get_results(self, class_name: str) -> ExtractedPlaylist:
        pass
