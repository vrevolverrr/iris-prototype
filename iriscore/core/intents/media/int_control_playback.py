# Builtins
from typing import Dict

# Core
from iriscore.core.enums import RequeryType, Status
from iriscore.core.request import RequeryRequest, RequestResult
from iriscore.core.structs.intent import Intent, IntentData, IntentUtterance, IntentResponse
from iriscore.core.structs.slot import Slot, SlotResult

# Entities
from iriscore.core.entities.ent_song import Song
from iriscore.core.entities.ent_platform import Platform
from iriscore.core.entities.ent_playback_control import PlaybackControl

# Modules
from iriscore.modules.Spotify import controller
from iriscore.modules.Spotify.spotify import SpotifyQueryType, SpotifyTrack

class ControlPlayback(Intent):
    @staticmethod
    def training_data() -> IntentData:
        return IntentData([
            IntentUtterance(Slot(PlaybackControl, "control"), "my playback"),
            IntentUtterance(Slot(PlaybackControl, "control"), " ", Slot(Platform, "platform"), "'s playback"),
            IntentUtterance(Slot(PlaybackControl, "control"), "playback on", Slot(Platform, "platform")),
            IntentUtterance(Slot(PlaybackControl, "control"), "the song on", Slot(Platform, "platform")),
            IntentUtterance(Slot(PlaybackControl, "control"), "this song on", Slot(Platform, "platform")),
            IntentUtterance("please", Slot(PlaybackControl, "control"), "my playback"),
            IntentUtterance("please", Slot(PlaybackControl, "control"), " ", Slot(Platform, "platform"), "'s playback"),
            IntentUtterance("please", Slot(PlaybackControl, "control"), "playback on", Slot(Platform, "platform")),
            IntentUtterance("please", Slot(PlaybackControl, "control"), "the song on", Slot(Platform, "platform")),
            IntentUtterance("please", Slot(PlaybackControl, "control"), "this song on", Slot(Platform, "platform")),
            IntentUtterance("pause", Slot(Song, "song"), "on", Slot(Platform, "platform")),
            IntentUtterance("please", Slot(PlaybackControl, "control"), " ", Slot(Song, "song"), "on", Slot(Platform, "platform"))
        ])

    @staticmethod
    def verify_slots( slot_results: Dict[str, SlotResult]) -> RequeryRequest:
        if "platform" not in slot_results.keys():
            return RequeryRequest("Whose playback would you like to me control?", "platform", Platform, RequeryType.KEYWORD)
    
        if "control" not in slot_results.keys():
            return RequeryRequest(f"What would you like me to do to {slot_results['platform'].value}?", "control", PlaybackControl, RequeryType.NATURAL)

        if slot_results["control"].value != "pause" and slot_results["control"].value != "resume":
            return RequeryRequest("Do you want to pause or resume your playback?", "control", PlaybackControl, RequeryType.NATURAL)

    @staticmethod
    def intent_action(input_text: str, slot_results: Dict[str, SlotResult]) -> IntentResponse[str]:
        if slot_results["platform"].value == "spotify":
                return ControlPlayback.platform_spotify(slot_results)
        else:
            return ControlPlayback.platform_others(slot_results)


    @staticmethod
    def intent_response(intent_response: IntentResponse[str]) -> RequestResult:
        return RequestResult(intent_response.results, Status.COMPLETED)

    @staticmethod
    def platform_spotify(slot_results: Dict[str, SlotResult]) -> IntentResponse[str]:
        spotify = controller.Spotify.get_instance()

        if "song" in slot_results.keys():
            track: SpotifyTrack = spotify.now_playing()
            if spotify.search(slot_results["song"].value, SpotifyQueryType.TRACK, limit=1)[0].name.lower() == track.name.lower():
                
                if slot_results["control"].value == "pause":
                    spotify.pause()
                elif slot_results["control"].value == "resume":
                    spotify.play()
                
                return IntentResponse(None)

            else:
                return IntentResponse("The song is not being played on Spotify")
        
        else:
            if slot_results["control"].value == "pause":
                spotify.pause()
            elif slot_results["control"].value == "resume":
                spotify.play()
            
            return IntentResponse(None)

    @staticmethod
    def platform_others(slot_results: Dict[str, SlotResult]):
        raise NotImplementedError("Intent action for platform others not provided")