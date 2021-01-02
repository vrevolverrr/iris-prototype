from snips_nlu import SnipsNLUEngine
from iriscore.core.config import MODEL_PATH

class NLUEngine:
    instance = None

    def __init__(self):
        try:
            assert self.engine
        except AttributeError:
            self.engine = SnipsNLUEngine.from_path(MODEL_PATH)
    
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        
        return cls.instance

    def parse(self, text: str, scope=None) -> dict:
        return self.engine.parse(text, intents=scope)

