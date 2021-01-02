import time
import spotipy
from typing import List, Union
from spotipy.oauth2 import SpotifyOAuth
from iriscore.modules.Spotify import client
from iriscore.modules.Spotify.spotify import SpotifyPlayer, SpotifyTrack, SpotifyArtist, SpotifyAlbum, SpotifyPlaylist, SpotifyQueryType

class Spotify:
    instance = None

    def __init__(self):
        raise NotImplementedError("Use classmethod get_instance to get an instance of the spotify controller")

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = SpotifyModule()

        return cls.instance

class SpotifyModule:
    def __init__(self):
        with open("./iriscore/modules/Spotify/user-scopes.dat", "r") as f:
            self.scope = f.read()

        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))

    def get_player(self):
        return SpotifyPlayer(self.client.current_playback())

    def now_playing(self):
        response = self.client.currently_playing()
        if response["is_playing"]:
            return SpotifyTrack(response["item"])

    def play(self) -> bool:
        if not self.now_playing():
           self.client.start_playback()
           return True
        else:
            return False

    def pause(self) -> bool:
        if self.now_playing():
            self.client.pause_playback()
            return True
        else:
            return False

    def set_volume(self, percent_int: int) -> None:
        player = self.get_player()

        return self.client.volume(percent_int, device_id=player.device.id)

    def prev_track(self):
        return self.client.previous_track()

    def next_track(self):
        return self.client.next_track()

    def search(self, query: str, result_type: SpotifyQueryType, limit=10) -> Union[List[SpotifyTrack], List[SpotifyArtist], List[SpotifyAlbum], List[SpotifyPlaylist]]:
        response = self.client.search(q=query, type=result_type.value, limit=limit)[result_type.value + "s"]["items"]

        if result_type == SpotifyQueryType.TRACK:
            return [SpotifyTrack(track) for track in response]
        elif result_type == SpotifyQueryType.ARTIST:
            return [SpotifyArtist(artist) for artist in response]
        elif result_type == SpotifyQueryType.ALBUM:
            return [SpotifyAlbum(album) for album in response]
        elif result_type == SpotifyQueryType.PLAYLIST:
            return [SpotifyPlaylist(playlist) for playlist in response]

    def add_to_queue_with_uri(self, track_uri, device_id=None):
        try:
            return self.client.add_to_queue(track_uri, device_id=device_id)
        except spotipy.SpotifyException:
            client.Client.start_playback()
            time.sleep(0.5)
            return self.add_to_queue_with_uri(track_uri, device_id=device_id)
        
    def play_track(self, track_name, track_artist: str = None):
        if track_artist is None:
            track: SpotifyTrack = self.search(query=track_name, result_type=SpotifyQueryType.TRACK, limit=1)[0]
        else:
            possible_tracks: List[SpotifyTrack] = self.search(query=track_name, result_type=SpotifyQueryType.TRACK, limit=10)
            artist: SpotifyArtist = self.search(track_artist, SpotifyQueryType.ARTIST, limit=1)[0]
            track = get_artist_matched_track(artist, possible_tracks)
        
        self.add_to_queue_with_uri(track.track_uri)
        self.next_track()

        time.sleep(0.5)
        return self.now_playing()

    def play_user_top_track(self, offset=0, time_range="short_term"):
        top_tracks = [SpotifyTrack(track) for track in self.client.current_user_top_tracks(limit=10, time_range=time_range)["items"]]

        self.add_to_queue_with_uri(top_tracks[offset % 20].track_uri)
        self.next_track()

        time.sleep(0.5)
        return self.now_playing()

    def play_user_top_artist(self, offset=0):
        top_artists = [SpotifyArtist(artist) for artist in self.client.current_user_top_artists(limit=5, time_range="short_term")["items"]]
        
        return self.play_artist_top_track(top_artists[offset % 5].name)

    def play_artist_top_track(self, artist_name, offset=0):
        artist = self.search(query=artist_name, result_type=SpotifyQueryType.ARTIST, limit=1)
        top_tracks = [SpotifyTrack(track) for track in self.client.artist_top_tracks(artist[0].artist_uri)["tracks"]]
        
        self.add_to_queue_with_uri(top_tracks[offset % 10].track_uri)
        self.next_track()

        time.sleep(0.5)
        return self.now_playing()
    
    def get_user_owned_playlists(self):
        current_user_id = self.client.current_user()["id"]
        return list(filter(lambda playlist: playlist["owner"]["id"] == current_user_id, self.client.current_user_playlists(limit=50)["items"]))

    def add_to_playlist(self, track_uri: str, playlist_uri: str):
        return self.client.playlist_add_items(playlist_uri.split(":")[2], [track_uri])

def get_artist_matched_track(artist: SpotifyArtist, possible_tracks: List[SpotifyTrack]):
    for possible_track in possible_tracks:
        artists =  [artist.lower() for artist in possible_track.artists]
        if artist.name.lower() in artists:
            return possible_track

    return possible_tracks[0]