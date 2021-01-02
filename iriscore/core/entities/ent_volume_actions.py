from iriscore.core.structs.entity import Entity, EntityData

class VolumeActions(Entity):
    isExtensible = False
    matchingStrictness = 1.0
    useSynonyms = True

    @staticmethod
    def training_data() -> EntityData:
        return EntityData([
            ["set", "adjust"],
            ["raise", "increase"],
            ["lower", "decrease"],
            ["mute", "silence"]
        ])