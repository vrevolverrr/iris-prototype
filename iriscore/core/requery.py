import pickle
import spacy
import iriscore.core.entities

from typing import Dict
from iriscore.core.config import ENTITIES_INDEX_PATH
from iriscore.core.request import RequeryRequest
from iriscore.core.enums import RequeryType
from iriscore.core.structs.intent import IntentResult
from iriscore.core.structs.entity import Entity
from iriscore.core.structs.slot import Slot, SlotResult

class RequeryParser:
    def __init__(self):
        with open(ENTITIES_INDEX_PATH, "rb") as f:
            self.entities: Dict[str, Entity] = pickle.load(f)
        
        self.nlp = spacy.load("en_core_web_lg")

    def parse(self, query: str, intent_result: IntentResult, requery_request: RequeryRequest) -> IntentResult:
        entity_name = requery_request.requery_entity.entity_name()

        if requery_request.requery_type == RequeryType.KEYWORD:
            slot_item = {"rawValue": query, "value": {"value": query}, "entity": entity_name, "slotName": requery_request.requery_item}
            intent_result.slots[requery_request.requery_item] = SlotResult(slot_item)

        elif requery_request.requery_type == RequeryType.NATURAL:
            matched_entity = self.match_entity(query, entity_name)
            
            if matched_entity is None:
                return None
            
            slot_item = {"rawValue": matched_entity, "value": {"value": matched_entity}, "entity": entity_name, "slotName": requery_request.requery_item}
            intent_result.slots[requery_request.requery_item] = SlotResult(slot_item)

        return intent_result

    def match_entity(self, query: str, entity_name: str):
        entity_data = self.entities[entity_name].training_data()
        similarities = dict()
        
        tokens = self.nlp(query)

        for token in tokens:
            for entity in entity_data:
                if type(entity) is list:
                    for synonym in entity:
                        entity_token = self.nlp(synonym)
                        similarities[token.similarity(entity_token)] = synonym
                else:
                    entity_token = self.nlp(entity)
                    similarities[token.similarity(entity_token)] = entity

        max_similarity = max(similarities.keys())
        return similarities[max_similarity] if max_similarity > 0.95 else None