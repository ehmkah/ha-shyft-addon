from sync_service import SyncService


import os
from flask import Flask, send_from_directory, jsonify, request
import threading, time
import requests
import json
import shutil

app = Flask(__name__, static_folder="www", static_url_path="")
sync_service = SyncService()
SHYFT_ACCESS_KEY = "not_set_yet"
OPTIONS_PATH = "/data/options.json"
CONFIG_PATH = "/data/config.json"
UPDATE_INTERVALL_IN_SECONDS = 3600
SUPERVISOR_TOKEN = value = os.getenv("SUPERVISOR_TOKEN")
HASSIO_URI_RUNNING_ON_HAOS = "http://supervisor/core"
HASSIO_URI_RUNNING_REMOTE = "http://homeassistant.local:8123"
# HASSIO_URI = HASSIO_URI_RUNNING_REMOTE
HASSIO_URI = HASSIO_URI_RUNNING_ON_HAOS

# Serve the static HTML
@app.route("/")
def index():
    return send_from_directory("www", "index.html")

# Delivers data to bubble
@app.route("/trigger", methods=["POST"])
def triggerEndpoint():
    return syncSensors()

def syncSensors():
    return sync_service.syncSensors()

def syncPVHistory():
    return sync_service.syncPVHistory()

@app.route("/config", methods=["GET"])
def readConfig():
    content = "nothing"
    with open(CONFIG_PATH, "r") as file:
        content = file.read()

    return content


@app.route("/sensorids", methods=["GET"])
def readSensorIds():
    response = getFromHA("/api/states")
    return mapToResponse(response)


def mapToResponse(response):
    result = []
    for item in response:
        unitOfMeasurement = item["attributes"].get("unit_of_measurement", "")
        result.append(item["entity_id"] + ":" + item["state"] + " " + unitOfMeasurement)
    return jsonify(result)


@app.route("/config", methods=["PUT"])
def writeConfig():
    content = request.get_data(as_text=True)
    data = json.loads(content)

    # iterate over key/value pairs
    for key, value in data.items():
        for inner_key, inner_value in value.items():
            data[key][inner_key] = inner_value.split(":", 1)[0]

    result = json.dumps(data)
    with open(CONFIG_PATH, "w") as file:
        file.write(result)

    return result


def loadSensorValueFor(key, bubbleSensorIdentifier):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    sensorId = data["sensorMappings"][key]
    try:
        sensorValue = loadEntityState(sensorId)
        return {
            "entity_id": key,
            "state": sensorValue["state"],
            "unit": sensorValue["unit"],
            "sensor": bubbleSensorIdentifier
        }
    except:
        return "exception" + key


def postToHA(path, body):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}"
    }
    completeUri = HASSIO_URI + path
    response = requests.post(completeUri, headers=headers, json=body)
    return response.json()


def callBubblePeriodically():
    while True:
        with app.app_context():
            syncSensors()
        time.sleep(UPDATE_INTERVALL_IN_SECONDS)


# thread = threading.Thread(target=callBubblePeriodically, daemon=True)
# thread.start()

if __name__ == "__main__":
    try:
        with open(OPTIONS_PATH, "r") as f:
            options = json.load(f)
            SHYFT_ACCESS_KEY = options.get("shyft_access_key", SHYFT_ACCESS_KEY)
        if not os.path.exists(CONFIG_PATH):
            print("File does not exists")
            shutil.copy("www/defaultShyftConfig.json", CONFIG_PATH)
        else:
            print("File does already exists. nothing was copied")  ##

    except Exception as e:
        print("Failed to load config from options.json:", e)


    print("TOKEN FOR HAOS_API", SUPERVISOR_TOKEN)
    print("Loaded SHYFT_ACCESS_KEY:", SHYFT_ACCESS_KEY)
    app.run(host="0.0.0.0", port=8080)
