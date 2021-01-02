from iriscore.core.structs.entity import Entity, EntityData

class Platform(Entity):
    isExtensible = False

    @staticmethod
    def training_data() -> EntityData:
        return EntityData([
            "spotify",
            "windows",
            ["chrome", "google chrome"],
            "discord"
        ])