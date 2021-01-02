import os
import pickle
import json
from typing import List
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
import iriscore.core.intents
import iriscore.core.entities
from iriscore.core.config import MODEL_PATH, ENTITIES_INDEX_PATH, INTENTS_INDEX_PATH
from iriscore.core.structs.intent import Intent
from iriscore.core.structs.entity import Entity

class Trainer:
    def __init__(self):
        self.intents: List[Intent] = Intent.__subclasses__()
        self.entities: List[Entity] = Entity.__subclasses__()
        self.engine = SnipsNLUEngine(config=CONFIG_EN)
        self.model_path = MODEL_PATH

    def parse_training_data(self):
        self.data = dict()
        self.data["language"] = "en"

        intents_index = dict()
        entities_index = dict()

        training_entities = dict()
        training_intents = dict()

        for entity in self.entities:
            entity_name = entity.entity_name()
            entities_index[entity_name] = entity
            training_entities[entity_name] = entity.parse()

        for intent in self.intents:
            intent_name = intent.intent_name()
            intents_index[intent_name] = intent
            training_intents[intent_name] = intent.parse()

        self.data["entities"] = training_entities
        self.data["intents"] = training_intents

        with open(INTENTS_INDEX_PATH, "wb") as f:
            pickle.dump(intents_index, f)


        with open(ENTITIES_INDEX_PATH, "wb") as f:
            pickle.dump(entities_index, f)

        return self.data

    def train_model(self):
        if os.path.exists(self.model_path):
            print("Do you want to retrain the model (y/n): ")
            
            if input() == "y":
                os.remove(self.model_path)
            else: return
        
        training_data = self.parse_training_data()

        self.engine.fit(training_data)
        self.engine.persist(self.model_path)

    def save_training_data(self, training_data=None):
        if training_data is None:
            training_data = self.parse_training_data()

        with open("D:\\PersonalProjects\\iris-core\\iriscore\\data\\training_data.json", "w") as f:
            json.dump(training_data, f, indent=2)

Trainer().train_model()