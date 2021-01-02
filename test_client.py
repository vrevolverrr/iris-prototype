import base64
import json
import requests
import numpy as np
import sounddevice as sd

class IrisClient:
    def __init__(self):
        self.pending_requests = dict()
        self.base_url = "http://127.0.0.1:5000/iris/v1/request"

    def make(self, query: str, request_id=None):
        request_data = dict()
        request_data["query"] = query
        request_data["request_id"] = request_id
        request_data["request_type"] = "query" if request_id is None else "requery"

        response = requests.post(self.base_url, json.dumps(request_data))
        response_data = json.loads(response.text)

        response_text: str = response_data["response_text"]

        if  response_data["response_audio"] is not None:
            response_audio: str =  response_data["response_audio"]
            audio_data = np.frombuffer(base64.b64decode(response_audio.encode('ascii')), dtype='float32')
            print(response_text)
            sd.play(audio_data, samplerate=22050)

        if response_data["status"] == "requery":
            requery_query = input()
            self.make(requery_query, request_id=response_data["request_id"])

    def remake(query: str, request_id: str):
        ...