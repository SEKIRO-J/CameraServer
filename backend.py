import threading
import time
import json

from flask import Flask, request
app = Flask(__name__)

camera_request = None
logs = None


@app.route("/getLogs", methods=['GET'])
def get_logs():
    """Endpoint for getting the logs. $curl localhost:8000/getLogs
    """
    global logs, camera_request
    logs = None
    camera_request = 'get_logs'
    while not logs:
        time.sleep(.01)
    return json.dumps(logs)


@app.route("/submitLogs", methods=['POST'])
def submit_logs():
    """Endpoint for the camera to submit logs
    """
    global logs
    logs = request.get_json()
    return ''


@app.route("/getRequest", methods=['POST'])
def get_request():
    """Endpoint for the camera to long poll while waiting for an action
    """
    global camera_request
    while not camera_request:
        time.sleep(.01)
    camera_request, send_request = None, camera_request
    return send_request


if __name__ == '__main__':
    app.run(debug=True)
