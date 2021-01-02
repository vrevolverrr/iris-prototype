import pickle
from iriscore.core.structs.entity import Entity, EntityData

class Song(Entity):
    matchingStrictness = 0.5

    @staticmethod
    def training_data() -> EntityData:
        with open("D:\\PersonalProjects\\iris-core\\iriscore\\data\\songs.dat", "rb") as f:
            song_data = pickle.load(f)

        return EntityData(song_data)