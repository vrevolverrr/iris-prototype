# Builtins
import base64
import json
import random
from snips_nlu import SnipsNLUEngine

# Core
from iriscore.core.config import MODEL_PATH, REQUEST_ID_LENGTH
from iriscore.core.enums import RequestType, Status
from iriscore.core.synthesizer.synthesizer import Synthesizer
from iriscore.core.structs.intent import IntentResponse, IntentResult
from iriscore.core.request import RequeryRequest
from iriscore.core.requery import RequeryParser

class Iris:
    engine: SnipsNLUEngine = None
    synthesizer: Synthesizer = None
    requery_parser: RequeryParser = None
    pending_requests = dict()

    @classmethod
    def start(cls):
        cls.engine = SnipsNLUEngine.from_path(MODEL_PATH)
        cls.synthesizer = Synthesizer()
        cls.requery_parser = RequeryParser()

    @staticmethod
    def handle_request(request_data: dict):
        iris_request = IrisRequest(request_data)
        iris_request.execute()

        return iris_request.response_string()

class IrisRequest:
    def __init__(self, request_data: dict):
        self.query: str = request_data["query"]
        self.request_id = request_data["request_id"]
        self.request_type: RequestType = IrisRequest.parse_request_type(request_data["request_type"])
        self.status: Status = Status.PENDING
        self.response_text: str = None
        self.response_audio: bytes = None

    def response_string(self):
        response: dict = dict()
        response["response_text"] = self.response_text
        response["response_audio"] = base64.b64encode(self.response_audio).decode('ascii')
        response["request_id"] = self.request_id
        response["status"] = self.status.value

        return json.dumps(response)

    def execute(self) -> None:
        if self.request_type is RequestType.QUERY:
            intent_result: IntentResult = IntentResult(Iris.engine.parse(self.query))
            requery_request: RequeryRequest = intent_result.intent_class.verify_slots(intent_result.slots)
        
        elif self.request_type is RequestType.REQUERY:
            pending_request = Iris.pending_requests[self.request_id]
            query_requery_request: RequeryRequest = pending_request["requery_request"]
            query_intent_result: IntentResult = pending_request["intent_result"]
            
            intent_result: IntentResult = Iris.requery_parser.parse(self.query, query_intent_result, query_requery_request)

            if intent_result is not None:  # Valid requery entitiy value
                requery_request: RequeryRequest = intent_result.intent_class.verify_slots(intent_result.slots)
            else:
                self.response_text = f"I'm sorry but {self.query} is not a valid {query_requery_request.requery_item}"
                self.response_audio = Iris.synthesizer.synthesize_speech(self.response_text)
                self.status = Status.INVALID
                return
            
            Iris.pending_requests.pop(self.request_id)
        
        else: return  # Dismiss request if invalid request type
        
        if requery_request is None:
            intent_response: IntentResponse = intent_result.intent_class.intent_action(intent_result.raw_text, intent_result.slots)
            self.response_text = intent_result.intent_class.intent_response(intent_response).result
            self.response_audio = Iris.synthesizer.synthesize_speech(self.response_text)
            self.status = Status.COMPLETED
        else:
            self.request_id = IrisRequest.generate_id(REQUEST_ID_LENGTH)
            pending_request = {"intent_result": intent_result, "requery_request": requery_request}
            Iris.pending_requests[self.request_id] = pending_request
            self.response_text = requery_request.requery_text
            self.response_audio = Iris.synthesizer.synthesize_speech(self.response_text)
            self.status = Status.REQUERY
            
    @staticmethod
    def generate_id(length, string="") -> str:
        strings = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        
        if len(string) < length:
            string += strings[random.randint(0, len(strings) - 1)]
            return IrisRequest.generate_id(length, string)
        else:
            return string

    @staticmethod
    def parse_request_type(request_type: str) -> RequestType:
        for item in RequestType:
            if request_type == item.value:
                return item

        return None