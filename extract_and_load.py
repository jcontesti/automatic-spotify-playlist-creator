import logging
import sys

from extraction_configuration.extraction_configuration_loader \
    import ExtractionConfigurationLoader
from spotify.spotify_session import SpotifySession
from extractors.extractor_factory import ExtractorFactory

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == "__main__":
    configuration_files = ExtractionConfigurationLoader().return_configuration_files()

    for configuration_file in configuration_files:
        spotify_playlist_destination = configuration_file.get_field(
            "spotify_playlist_destination"
        )
        only_load_songs_released_in_last_year = configuration_file.get_field(
            "only_load_songs_released_in_last_year"
        ) or False
        load_all_songs_from_albums = configuration_file.get_field(
            "load_all_songs_from_albums"
        ) or False

        session = SpotifySession()

        # Extract all songs
        module_name = configuration_file.get_extractor_module_name()
        class_name = configuration_file.get_extractor_class_name()
        extractor = ExtractorFactory.get_extractor(module_name, class_name)

        print(extractor)

        extracted_playlist = extractor.extract_playlist()

        # Clean extracted songs
        extracted_playlist.clean_playlist()

        # Convert extracted songs to a Spotify playlist
        session.replace_spotify_playlist_from_extracted_playlist(
            spotify_playlist_destination=spotify_playlist_destination,
            extracted_playlist=extracted_playlist,
            only_load_songs_released_in_last_year=only_load_songs_released_in_last_year,
            load_all_songs_from_albums=load_all_songs_from_albums,
        )
