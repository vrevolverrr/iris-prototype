from enum import Enum
from typing import List, Dict
from typing_extensions import Literal

class SpotifyPlayer:
    def __init__(self, playback_response: dict):
        if playback_response is None:
            raise SpotifyNotActive("No active Spotify playback device could be found")

        self.now_playing = SpotifyTrack(playback_response["item"])
        self.device = SpotifyPlaybackDevice(playback_response["device"])
        self.progress: int = playback_response["progress_ms"]
        self.isPlaying: bool = playback_response["is_playing"]
        self.isShuffle: bool = playback_response["shuffle_state"]
        self.isRepeat: bool = playback_response["repeat_state"]

class SpotifyTrack:
    def __init__(self, item_response):
            self.name: str = item_response["name"]
            self.track_duration: int = item_response["duration_ms"]
            self.track_uri: str = item_response["uri"]
            self.artists: List[str] = [artist["name"] for artist in item_response["artists"]]
            self.album: str = item_response["album"]["name"]
            self.album_release_date: str = item_response["album"]["release_date"]
            self.album_num_tracks: int = item_response["album"]["total_tracks"]
            self.album_uri: str = item_response["album"]["uri"]
            self.thumbnail: Dict[Literal] = {"sm": item_response["album"]["images"][2]["url"],
                                    "md": item_response["album"]["images"][1]["url"],
                                    "lg": item_response["album"]["images"][0]["url"]}

class SpotifyArtist:
    def __init__(self, item_response: dict):
        self.name: str = item_response["name"]
        self.followers: int = item_response["followers"]["total"]
        self.genres: List[str] = item_response["genres"]
        self.artist_uri: str = item_response["uri"]

class SpotifyAlbum:
    def __init__(self, item_response: dict):
        self.name: str = item_response["name"]
        self.album_type = item_response["album_type"]
        self.album_release_date: str = item_response["release_date"]
        self.album_num_tracks: int = item_response["total_tracks"]
        self.album_uri: str = item_response["uri"]
        self.artists: List[str] = [artist["name"] for artist in item_response["artists"]]
        self.thumbnail: dict = {"sm": item_response["images"][2]["url"],
                                "md": item_response["images"][1]["url"],
                                "lg": item_response["images"][0]["url"]}

class SpotifyPlaylist:
    def __init__(self, item_response: dict):
        self.name: str = item_response["name"]
        self.description: str = item_response["description"]
        self.playlist_num_tracks: int = item_response["tracks"]["total"]
        self.playlist_owner: str = item_response["owner"]["display_name"]
        self.playlist_owner_uri: str = item_response["owner"]["uri"]
        self.playlist_uri: str = item_response["uri"]
        self.thumbnail: dict = {"lg": item_response["images"][0]["url"]}

class SpotifyPlaybackDevice:
    def __init__(self, device_response: dict):
        self.id: str = device_response["id"]
        self.name: str = device_response["name"]
        self.type: str = device_response["type"]
        self.volume: int = device_response["volume_percent"]
        self.isActive: bool = device_response["is_active"]
        self.isPrivate: bool = device_response["is_private_session"]
        self.isRestricted: bool = device_response["is_restricted"]

class SpotifyQueryType(Enum):
    TRACK = "track"
    PLAYLIST = "playlist"
    ARTIST = "artist"
    ALBUM = "album"

class SpotifyNotActive(Exception): ...