import os
from flask import Flask, send_from_directory, jsonify, request
import threading, time
import requests
import json
import datetime
import shutil

app = Flask(__name__, static_folder="www", static_url_path="")
SHYFT_ACCESS_KEY = "not_set_yet"
OPTIONS_PATH = "/data/options.json"
CONFIG_PATH = "/data/config.json"
UPDATE_INTERVALL_IN_SECONDS=3600
SUPERVISOR_TOKEN = value = os.getenv("SUPERVISOR_TOKEN")
HASSIO_URI_RUNNING_ON_HAOS = "http://supervisor/core"
HASSIO_URI_RUNNING_REMOTE = "http://homeassistant.local:8123"
HASSIO_URI = HASSIO_URI_RUNNING_ON_HAOS

LIST_OF_SENSORS = [
"photovoltaic_powerflow_pv",
"photovoltaic_powerflow_load",
"photovoltaic_powerflow_grid",
"photovoltaic_powerflow_battery",
"battery_storage_command_mode",
"battery_state_of_charge",
"battery_discharge_limit_current",
"battery_charge_limit_current"
]


# Serve the static HTML
@app.route("/")
def index():
    return send_from_directory("www", "index.html")


# Delivers data to bubble
@app.route("/trigger", methods=["POST"])
def triggerEndpoint():
    return trigger()

def trigger():
    try:
        sensorValues = []
        for sensor in LIST_OF_SENSORS:
             valueForSensor = loadSensorValueFor(sensor)
             if valueForSensor != "":
                 sensorValues.append(valueForSensor)
        payload = ""
        if len(sensorValues) > 0:
            payload = "&".join(sensorValues)

        headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {SHYFT_ACCESS_KEY}"
            }
        external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/obj/homeassistanttest"
        response = requests.post(external_url, headers=headers, data=payload)
        return jsonify({
         "status": "success",
         "payload" : payload,
         "external_status": response.status_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/config", methods=["GET"])
def readConfig():
    content = "nothing"
    with open(CONFIG_PATH, "r") as file:
        content = file.read()

    return content

@app.route("/togglewaterheater", methods=["POST"])
def toggle():
    #currentState = loadEntityState("water_heater.heatpump_mock_the_mock")
    body = { "entity_id": "water_heater.heatpump_mock_the_mock" }
    postToHA("/api/services/water_heater/turn_on", body )
    content = {"status" : "OK"}

    return content


@app.route("/sensorids", methods=["GET"])
def readSensorIds():
    response = getFromHA("/api/states")
    return jsonify([item["entity_id"] for item in response])

@app.route("/config", methods=["PUT"])
def writeConfig():
    content = request.get_data(as_text=True)

    with open(CONFIG_PATH, "w") as file:
        file.write(content)

    return content

def loadSensorValueFor(key):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    sensorId = data[key]
    sensorValue="unset"
    try:
        sensorValue=loadEntityState(sensorId)
        return f"{key}={sensorValue}"
    except:
        return ""

def loadEntityState(sensorId):
    response = getFromHA("/api/states/"+sensorId)
    return response["state"]

def getFromHA(path):
    headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {SUPERVISOR_TOKEN}"
                }
    completeUri = HASSIO_URI+path
    response =  requests.get(completeUri, headers=headers)
    return response.json()


def postToHA(path, body):
    headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {SUPERVISOR_TOKEN}"
                }
    completeUri = HASSIO_URI+path
    response =  requests.post(completeUri, headers=headers, json=body)
    return response.json()

def callBubblePeriodically():
    while True:
        with app.app_context():
            trigger()
        time.sleep(UPDATE_INTERVALL_IN_SECONDS)

# Enable before merge
#thread = threading.Thread(target=callBubblePeriodically, daemon=True)
#thread.start()

if __name__ == "__main__":
    try:
        with open(OPTIONS_PATH, "r") as f:
            options = json.load(f)
            SHYFT_ACCESS_KEY = options.get("shyft_access_key", SHYFT_ACCESS_KEY)
        if not os.path.exists(CONFIG_PATH):
            print("File does not exists")
            shutil.copy("www/defaultShyftConfig.json", CONFIG_PATH)
        else:
            print("File does already exists. nothing was copied")##

    except Exception as e:
        print("Failed to load config from options.json:", e)

    print("TOKEN FOR HAOS_API", SUPERVISOR_TOKEN)
    print("Loaded SHYFT_ACCESS_KEY:", SHYFT_ACCESS_KEY)
    app.run(host="0.0.0.0", port=8080)
