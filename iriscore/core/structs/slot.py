import random
from iriscore.core.structs.entity import Entity

class Slot:
    def __init__(self, entity: Entity, slot_name: str):
        self.entity = entity
        self.slot_name = slot_name
    
    def parse(self):
        entity_data = dict()

        entity_data["entity"] = self.entity.entity_name()
        entity_data["slot_name"] = self.slot_name

        rand_entity = random.choice(self.entity.training_data())
        if type(rand_entity) is list:
            entity_data["text"] = random.choice(rand_entity)
        else:
            entity_data["text"] = rand_entity

        return entity_data

    def __repr__(self):
        return self.parse()["text"]

class SlotResult:
    def __init__(self, slot_item: dict):
        self.raw_value = slot_item["rawValue"]
        self.value = slot_item["value"]["value"]
        self.entity = slot_item["entity"]
        self.slot_name = slot_item["slotName"]
        # self.start = slot_item["range"]["start"]
        # self.end = slot_item["range"]["end"]