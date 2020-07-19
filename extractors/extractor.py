from abc import ABC, abstractmethod
from extracted_data.extracted_playlist import ExtractedPlaylist


class Extractor(ABC):
    @abstractmethod
    def extract_playlist(self) -> ExtractedPlaylist:
        pass
