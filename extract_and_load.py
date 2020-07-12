import logging
import sys

from extraction_configuration.extraction_configuration_loader \
    import ExtractionConfigurationLoader
from spotify.spotify_session import SpotifySession
from extracted_data.extracted_playlist import ExtractedPlaylist

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == "__main__":
    configuration_files = ExtractionConfigurationLoader().return_configuration_files()

    for configuration_file in configuration_files:
        spotify_playlist_destination = configuration_file.get_field("spotify_playlist_destination")

        session = SpotifySession()

        # Extract all songs to load from source
        extracted_playlist = configuration_files.get_extractor().get_results()
        extracted_playlist.clean_playlist()

        # Convert extracted songs to a Spotify playlist
        SpotifyPlaylist = session.get_spotify_playlist_from_extracted_playlist(
            spotify_playlist_destination=spotify_playlist_destination,
            extracted_playlist=extracted_playlist,
        )






        self._get_new_songs_to_load()

        playlist_current_songs = self._get_playlist_current_songs()

        # Remove all current songs that have gone out of the playlist
        self._remove_deleted_songs(playlist_current_songs)

        # Add all the new songs that weren't on the playlist
        self._add_new_songs(playlist_current_songs)

        # playlist_config = read_yaml(config_file)
        #
        # spider_class_name = playlist_config.get("spider_class")
        #
        # # @TODO: return Playlist
        # scrapped_songs = scrappy_loader.get_results(spider_class_name)
        #
        # if scrapped_songs:
        #     spotify_playlist = playlist_config.get("spotify_playlist")
        #     spotify_session = spotipy.Spotify(auth=token)
        #     spotify_username = settings.SPOTIFY_USERNAME
        #     spotify_country = playlist_config.get("spotify_country")
        #     spotify_ignored_tracks = playlist_config.get("spotify_ignored_tracks")
        #     artists_split = playlist_config.get("artists_split")
        #     songs_titles_split = playlist_config.get("songs_titles_split")
        #     get_full_albums = playlist_config.get(
        #         "get_full_albums"
        #     )
        #     get_only_most_played_songs_from_albums = playlist_config.get(
        #         "get_only_most_played_songs_from_albums"
        #     )
        #     check_released_last_year = playlist_config.get("check_released_last_year")
        #     artists_transformations = playlist_config.get("artists_transformations")
        #     misspelling_correctors = playlist_config.get("misspelling_correctors")
        #
        #     scrapped_playlist = ExtractedPlaylistOld(
        #         spotify_playlist,
        #         spotify_session,
        #         spotify_username,
        #         spotify_country,
        #         scrapped_songs,
        #         spotify_ignored_tracks,
        #         artists_split,
        #         songs_titles_split,
        #         get_full_albums,
        #         get_only_most_played_songs_from_albums,
        #         check_released_last_year,
        #         artists_transformations,
        #         misspelling_correctors,
        #     )
        #
        #     scrapped_playlist.update_playlist()
