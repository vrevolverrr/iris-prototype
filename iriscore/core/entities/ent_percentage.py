from iriscore.core.entities.builtin_ents import BuiltinEntities
from iriscore.core.structs.entity import Entity, EntityData

class Percentage(Entity):
    useBuiltins = BuiltinEntities.Percentage

    @staticmethod
    def training_data() -> EntityData:
        return EntityData([
            "20%", "13%", "100%", "fourty five percent", "twenty five percents", "eighty percent", "one hundred and thirty percents"
        ])