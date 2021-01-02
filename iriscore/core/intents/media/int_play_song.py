# Builtin
import random
from typing import Dict

# Core
from iriscore.core.enums import RequeryType, Status
from iriscore.core.request import RequestResult, RequeryRequest
from iriscore.core.structs.slot import Slot, SlotResult
from iriscore.core.structs.intent import Intent, IntentData, IntentUtterance, IntentResponse

# Entities
from iriscore.core.entities.ent_song import Song
from iriscore.core.entities.ent_artist import Artist
from iriscore.core.entities.ent_platform import Platform

# Modules
from iriscore.modules.Spotify.spotify import SpotifyTrack
from iriscore.modules.Spotify import controller

class PlaySong(Intent):
    def __init__(self):
        super.__init__()

    @staticmethod
    def training_data() -> IntentData:
        return IntentData([
            IntentUtterance("play", Slot(Artist, "artist"), "'s", Slot(Song, "song"), "on", Slot(Platform, "platform")),
            IntentUtterance("play", Slot(Artist, "artist"), "'s", Slot(Song, "song"), "on", Slot(Platform, "platform")),
            IntentUtterance("play", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("play me", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("please play me", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("please play", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("can you play", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("could you please play", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("i would like to listen to", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
            IntentUtterance("i want to listen to", Slot(Song, "song"), "by", Slot(Artist, "artist"), "on", Slot(Platform, "platform")),
        ])

    @staticmethod
    def verify_slots(slot_results: Dict[str, SlotResult]) -> RequeryRequest:
        if "song" not in slot_results.keys():
            return RequeryRequest("What would you like to listen to?", "song", Song, RequeryType.KEYWORD)

    @staticmethod
    def intent_action(input_text: str, slot_results: Dict[str, SlotResult]) -> IntentResponse[SpotifyTrack]:
        spotify = controller.Spotify.get_instance()
        
        any_track_words = ["song", "anything", "something"]
        top_track_quotes = ["my top song", "my favourite song", "my top track", "my favourite track", "something i like", "something i love"]

        if slot_results["song"].raw_value in any_track_words:
            if "artist" in slot_results.keys():
                return IntentResponse(spotify.play_artist_top_track(slot_results["artist"].raw_value))
            else:
                return IntentResponse(spotify.play_user_top_track(offset=random.randint(0, 10), time_range="medium_term"))
        
        elif slot_results["song"].raw_value in top_track_quotes and "artist" not in slot_results.keys():
            return IntentResponse(spotify.play_user_top_track())

        if "artist" in slot_results.keys():
            return IntentResponse(spotify.play_track(slot_results["song"].raw_value, slot_results["artist"].raw_value))
        else:
            return IntentResponse(spotify.play_track(slot_results["song"].raw_value))

    @staticmethod
    def intent_response(intent_response: IntentResponse[SpotifyTrack]) -> RequestResult:
        artists = intent_response.results.artists

        if len(artists) == 1:
            artist_string = artists[0]
        
        elif len(artists) == 2:
            artist_string = ' and '.join(artists)
        
        else:
            artist_string = ', '.join(artists[:-1]) + " and " + artists[-1]

        return RequestResult(f"Now playing {intent_response.results.name} by {artist_string}", Status.COMPLETED)