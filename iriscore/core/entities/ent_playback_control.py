from iriscore.core.structs.entity import Entity, EntityData

class PlaybackControl(Entity):
    isExtensible = False
    matchingStrictness = 1.0
    useSynonyms = True

    @staticmethod
    def training_data() -> EntityData:
        return EntityData([
            ["resume", "play"],
            ["pause", "stop"]
        ])