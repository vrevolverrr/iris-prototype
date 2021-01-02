import pickle
from iriscore.core.structs.entity import Entity, EntityData

class Artist(Entity):
    matchingStrictness = 0.5

    def training_data() -> EntityData:
        with open("D:\\PersonalProjects\\iris-core\\iriscore\\data\\artists.dat", "rb") as f:
            artist_dat = pickle.load(f)
        
        return EntityData(artist_dat)