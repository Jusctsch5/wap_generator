from playlist import Playlist
from types import SimpleNamespace
import json

class PlaylistDecoder:

    """
     PlaylistDecoder - Decodes input json Playlist file and creates a Playlist class
    """

    def __init__(self):
        pass

    def __decode_playlist(self, playlist_filename, configuration):
        with open(playlist_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        playlist = Playlist(x)
        return playlist

    def decode_playlist(self, playlist_filename, configuration):
        return self.__decode_playlist(playlist_filename, configuration)
