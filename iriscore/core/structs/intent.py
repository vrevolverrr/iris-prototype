# Builtin
import pickle
from typing import List, Dict, Union, Generic, TypeVar

# Core
from iriscore.core.config import INTENTS_INDEX_PATH
from iriscore.core.request import RequestResult, RequeryRequest
from iriscore.core.structs.slot import Slot, SlotResult

T = TypeVar("T")

class IntentResponse(Generic[T]):
    def __init__(self, results: any):
        self.results: T = results if results is not None else ""

class IntentUtterance:
    def __init__(self, *subutterances: List[Union[str, Slot]]):
        self.subutterances: List[Union[str, Slot]] = subutterances

    def __repr__(self):
        return " ".join([str(subutterance) for subutterance in self.subutterances])

    def parse(self):
        utterance_data = dict()
        data = list()

        for i in range(len(self.subutterances)):
            if type(self.subutterances[i]) is Slot:
                data.append(self.subutterances[i].parse())
            else:
                front_padding = " " if i - 1 >= 0 and type(self.subutterances[i - 1]) is Slot and not self.subutterances[i].startswith("'s") else ""
                end_padding = "" if i == (len(self.subutterances) - 1) else " "

                data.append({
                    "text": front_padding + str(self.subutterances[i]) + end_padding
                })

        utterance_data["data"] = data
        return utterance_data
            
class IntentData:
    def __init__(self, utterances: List[IntentUtterance]):
        self.utterances = utterances

    def parse(self):
        intent_data = dict()
        utterances_data = []

        for utterance in self.utterances:
            utterances_data.append(utterance.parse())

        intent_data["utterances"] = utterances_data
        return intent_data

    def __repr__(self):
        return repr(self.utterances)

    def __getitem__(self, i):
        return self.utterances[i]

class Intent:
    def __init__(self):
        raise TypeError("Intents should not be instantiated")
    
    @classmethod
    def intent_name(cls):
        intent_name = list(cls.__name__)
        intent_name[0] = intent_name[0].lower()
        
        return "".join(intent_name)

    @classmethod
    def parse(cls):
        return cls.training_data().parse()

    @staticmethod
    def training_data() -> IntentData:
        """
        Returns the actual intent utterances.
        """
        raise NotImplementedError("Training data not provided")
    
    @staticmethod
    def verify_slots(slot_results: Dict[str, SlotResult]) -> RequeryRequest:
        raise NotImplementedError("Verify Slots not implemented")

    @staticmethod
    def intent_action(input_text: str, slot_results: Dict[str, SlotResult]) -> IntentResponse[T]:
        raise NotImplementedError("Intent Action not implemented")

    @staticmethod
    def intent_response(intent_response: IntentResponse) -> RequestResult:
        raise NotImplementedError("Intent Response not implemented")

class IntentResult:
    with open(INTENTS_INDEX_PATH, "rb") as f:
            intents_index = pickle.load(f)

    def __init__(self, parsed_result: dict):
        if self.intents_index is None:
            raise AttributeError("Intents index not loaded. Please load it with load_intents()")

        self.raw_text: str = parsed_result["input"]
        self.intent_name: str = parsed_result["intent"]["intentName"]
        self.intent_probability: float = parsed_result["intent"]["probability"]
        self.intent_class: Intent = self.intents_index[self.intent_name]
        self.slots: Dict[str, SlotResult] = {slot["slotName"]: SlotResult(slot) for slot in parsed_result["slots"]}