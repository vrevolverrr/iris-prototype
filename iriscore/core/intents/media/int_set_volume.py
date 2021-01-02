# Builtins
from typing import Dict

# Core
from iriscore.core.enums import RequeryType, Status
from iriscore.core.request import RequestResult, RequeryRequest
from iriscore.core.structs.slot import Slot, SlotResult
from iriscore.core.structs.intent import Intent, IntentData, IntentUtterance, IntentResponse

# Entities
from iriscore.core.entities.ent_platform import Platform
from iriscore.core.entities.ent_percentage import Percentage
from iriscore.core.entities.ent_preposition import Preposition
from iriscore.core.entities.ent_volume_actions import VolumeActions

# Modules
from iriscore.modules.Spotify import controller

class SetVolume(Intent):
    @staticmethod
    def training_data() -> IntentData:
        return IntentData([
            # Partial
            IntentUtterance(Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform")),
            IntentUtterance(Slot(VolumeActions, "action"), "volume", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),

            # Complete
            IntentUtterance(Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance(Slot(VolumeActions, "action"), "the volume on", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("please", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("please", Slot(VolumeActions, "action"), "the volume on", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("can you please", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("could you please", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("would you please", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("can you", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("can you please", Slot(VolumeActions, "action"), "the volume on", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("could you", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
            IntentUtterance("would you", Slot(VolumeActions, "action"), "the volume of", Slot(Platform, "platform"), " ", Slot(Preposition, "prep"), " ", Slot(Percentage, "percent")),
        ])

    @staticmethod
    def verify_slots(slot_results: Dict[str, SlotResult]) -> RequeryRequest:
        if "platform" not in slot_results.keys():
            return RequeryRequest("Whose volume do you want to adjust?", "platform", Platform, RequeryType.KEYWORD)

        if "action" not in slot_results.keys():
            return RequeryRequest("What would you like me to do with the volume?", "action", VolumeActions, RequeryType.NATURAL)

        action = slot_results["action"].value
        possible_actions = ["raise", "lower", "set", "mute"]

        if action not in possible_actions:
            return RequeryRequest("What would you like me to do with the volume?", "action", VolumeActions, RequeryType.NATURAL)

        if action == "set" and "percent" not in slot_results.keys():
            return RequeryRequest("What volume do you want me to set it to?")

        if "percent" in slot_results.keys():
            if slot_results["percent"].value < 0 or slot_results["percent"].value > 100:
                return RequeryRequest("Please specify a volume in between 0 to 100 percent", Percentage, RequeryType.KEYWORD)

            if slot_results["action"].value == "raise" or slot_results["action"].value == "lower":
                if slot_results["prep"].value != "to" and slot_results["prep"].value != "by":
                    return RequeryRequest(f"Do you want me to {action} the volume to {slot_results['percent'].value} or {action} it by {slot_results['percent'].value}", "prep", Preposition, RequeryType.NATURAL)

    @staticmethod
    def intent_action(input_text: str, slot_results: Dict[str, SlotResult]) -> IntentResponse[None]:
        if slot_results["platform"].raw_value == "spotify":
            spotify = controller.Spotify.get_instance()

            if slot_results["action"].value == "raise":
                return IntentResponse(SetVolume.raise_volume(spotify, slot_results))
            elif slot_results["action"].value == "lower":
                return IntentResponse(SetVolume.lower_volume(spotify, slot_results))
            elif slot_results["action"].value == "set":
                return IntentResponse(SetVolume.set_volume(spotify, slot_results))
            elif slot_results["action"].value == "mute":
                return IntentResponse(spotify.set_volume(0))
        else:
            raise NotImplementedError("Other platforms not implemented")

    @staticmethod
    def intent_response(intent_response: IntentResponse) -> RequestResult:
        return RequestResult(intent_response.results, Status.COMPLETED)

    @staticmethod
    def raise_volume(spotify_instance: controller.SpotifyModule, slot_results: Dict[str, SlotResult]):
        current_volume: int = spotify_instance.get_player().device.volume

        if "percent" in slot_results.keys():
            if slot_results["percent"].value == current_volume:
                return

            if slot_results["prep"].raw_value == "to":
                if slot_results["percent"].value < current_volume:
                    return "The specified volume is lower than the current volume"

                spotify_instance.set_volume(int(slot_results["percent"].value))
                
            elif slot_results["prep"].raw_value == "by":
                spotify_instance.set_volume(int((current_volume + slot_results["percent"].value) % 101))

        else:
            spotify_instance.set_volume(int((current_volume + 30) % 101))

    @staticmethod
    def lower_volume(spotify_instance: controller.SpotifyModule, slot_results: Dict[str, SlotResult]):
        current_volume: int = spotify_instance.get_player().device.volume
        
        if "percent" in slot_results.keys():
            if slot_results["percent"].value == current_volume:
                return

            if slot_results["prep"].raw_value == "to":
                if slot_results["percent"].value > current_volume:
                    return "The specified volume is higher than the current volume"

                spotify_instance.set_volume(int(slot_results["percent"].value))

            elif slot_results["prep"].raw_value == "by":                
                volume = int(current_volume - slot_results["percent"].value if current_volume >= slot_results["percent"].value else 0)
                spotify_instance.set_volume(volume)
            
        else:
            volume = int(current_volume - 30 if current_volume >= 30 else 0)
            spotify_instance.set_volume(volume)

    @staticmethod
    def set_volume(spotify_instance: controller.SpotifyModule, slot_results: Dict[str, SlotResult]):
        current_volume: int = spotify_instance.get_player().device.volume
            
        if slot_results["percent"].value == current_volume:
            return

        spotify_instance.set_volume(int(slot_results["percent"].value))    