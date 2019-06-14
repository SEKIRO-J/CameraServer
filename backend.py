import threading
import time
import json

from flask import Flask, request
app = Flask(__name__)

request_id = None # to identify which camera's logs to query
camera_request = None
logs = None
state = None
event = threading.Event()

@app.route("/getState", methods=['GET'])
def get_state():
    """Endpoint for getting the state. $curl localhost:5000/getState
    """
    global state, camera_request, event
    sate = None
    camera_request = 'get_state'
    event.wait() # wait for submitLogs to complete
    event.clear() # clean the internal flag for this event
    return state

@app.route("/submitState", methods=['POST'])
def submit_state():
    """Endpoint for the camera to submit logs
    """
    global state, event
    state = request.data
    event.set() # set the flag, so get_logs can proceed
    return ''

@app.route("/getLogs/<id>", methods=['GET'])
def get_logs(id):
    """Endpoint for getting the logs. $curl localhost:5000/getLogs
    """
    global logs, camera_request, event, request_id
    logs = None
    request_id = id
    camera_request = 'get_logs'
    event.wait() # wait for submitLogs to complete
    event.clear() # clean the internal flag for this event
    return json.dumps(logs)


@app.route("/submitLogs", methods=['POST'])
def submit_logs():
    """Endpoint for the camera to submit logs
    """
    global logs, event
    logs = request.get_json()
    event.set() # set the flag, so get_logs can proceed
    return ''


@app.route("/getRequest/<id>", methods=['POST'])
def get_request(id):
    """Endpoint for the camera to long poll while waiting for an action
    """
    global camera_request, request_id
    while (not camera_request or request_id != id): # if the camera ids don't match, keep sleeping
        time.sleep(.01)
    camera_request, send_request = None, camera_request
    return send_request


if __name__ == '__main__':
    app.run(debug=True)
