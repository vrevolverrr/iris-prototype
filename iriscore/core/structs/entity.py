from typing import List

class EntityData:
    def __init__(self, data: List[str]):
        if type(data) is not list: raise TypeError("Expected type list")
        self.data = data

    def parse(self):
        entity_data = list()

        for entity in self.data:
            data = dict()
            if type(entity) is list:
                data["value"] = entity[0]
                data["synonyms"] = entity[1:]
            else:
                data["value"] = entity
                data["synonyms"] = []

            entity_data.append(data)

        return entity_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

class Entity:
    isExtensible: bool = True
    useSynonyms: bool = True
    matchingStrictness: float = 1.0
    useBuiltins = None

    @classmethod
    def entity_name(cls) -> str:
        return cls.useBuiltins.value if cls.useBuiltins else cls.__name__.lower()

    @staticmethod
    def training_data() -> EntityData:
        """
        Returns the actual entity data.
        Use nested arrays for synonyms with the first element as the actual value.
        Syntax: EntityData(["red", ["green", "greenish"]])
        """
        ...
    
    @classmethod
    def parse(cls):
        entity_data = dict()

        if not cls.useBuiltins:
            entity_data["automatically_extensible"] = cls.isExtensible
            entity_data["use_synonyms"] = cls.useSynonyms
            entity_data["matching_strictness"] = cls.matchingStrictness
            entity_data["data"] = cls.training_data().parse()

        return entity_data