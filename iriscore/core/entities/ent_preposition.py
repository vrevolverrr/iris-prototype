from iriscore.core.structs.entity import Entity, EntityData

class Preposition(Entity):
    isExtensible = False

    @staticmethod
    def training_data() -> EntityData:
        return EntityData(["to", "by"])