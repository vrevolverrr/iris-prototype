from iriscore.core.enums import Status, RequeryType
from iriscore.core.structs.entity import Entity

class RequeryRequest:
    def __init__(self, requery_text: str, requery_item: str, requery_entity: Entity, requery_type: RequeryType):
        self.requery_text: str = requery_text
        self.requery_item: str = requery_item
        self.requery_entity: Entity = requery_entity
        self.requery_type: RequeryType = requery_type

class RequestResult:
    def __init__(self, result: str, status: Status):
        self.result = result
        self.status = status
