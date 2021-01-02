from enum import Enum

class Status(Enum):
    PENDING = "pending"
    REQUERY = "requery"
    INVALID = "invalid"
    COMPLETED = "completed"

class RequestType(Enum):
    QUERY = "query"
    REQUERY = "requery"

class RequeryType(Enum):
    NATURAL = "natural"
    KEYWORD = "keyword"