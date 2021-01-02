import pickle
import iriscore.core.entities

from typing import Dict
from iriscore.core.config import ENTITIES_INDEX_PATH
from iriscore.core.nlu_engine import NLUEngine
from iriscore.core.request import RequeryRequest
from iriscore.core.enums import RequeryType
from iriscore.core.structs.intent import IntentResult
from iriscore.core.structs.entity import Entity
from iriscore.core.structs.slot import SlotResult

class RequeryParser:
    def __init__(self):
        self.engine: NLUEngine = NLUEngine()

        with open(ENTITIES_INDEX_PATH, "rb") as f:
            self.entities: Dict[str, Entity] = pickle.load(f)

    def parse(self, query: str, intent_result: IntentResult, requery_request: RequeryRequest) -> IntentResult:
        entity_name = requery_request.requery_entity.entity_name()

        if requery_request.requery_type == RequeryType.KEYWORD:
            slot_item = {"rawValue": query, "value": {"value": query}, "entity": entity_name, "slotName": requery_request.requery_item}
            intent_result.slots[requery_request.requery_item] = SlotResult(slot_item)

        elif requery_request.requery_type == RequeryType.NATURAL:
            intent_scope = [intent_result.intent_class.intent_name()]
            parsed_result = self.engine.parse(query, scope=intent_scope)
            slot_results = {slot["slotName"]: SlotResult(slot) for slot in parsed_result["slots"]}

            intent_result.slots.update(slot_results)

        return intent_result