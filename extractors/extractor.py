"""
Base class to implement playlist extractors.

This class should be extended and never instantiated.
"""
from abc import ABC, abstractmethod
from extracted_data.extracted_playlist import ExtractedPlaylist


class Extractor(ABC):
    """
    Base class to implement playlist extractors.

    The method 'extract_playlist' must be implemented in a new class that extends this one.
    """
    @abstractmethod
    def extract_playlist(self) -> ExtractedPlaylist:
        """Extract a playlist using an extractor, for instance, Scrapy."""
