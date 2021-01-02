import json
import flask
from iriscore.core.iris import Iris

app = flask.Flask(__name__)

@app.route('/iris/v1/request')
def iris_request():
    request_data = json.loads(flask.request.get_data())
    response_data = Iris.handle_request(request_data)

    return response_data

if __name__ == "__main__":
    Iris.start()
    app.run()