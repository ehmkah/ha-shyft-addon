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
UPDATE_INTERVALL_IN_SECONDS = 3600
SUPERVISOR_TOKEN = value = os.getenv("SUPERVISOR_TOKEN")
HASSIO_URI_RUNNING_ON_HAOS = "http://supervisor/core"
HASSIO_URI_RUNNING_REMOTE = "http://homeassistant.local:8123"
# HASSIO_URI = HASSIO_URI_RUNNING_REMOTE
HASSIO_URI = HASSIO_URI_RUNNING_ON_HAOS

LIST_OF_SENSORS = {
    "photovoltaic_powerflow_pv": "PV - PowerFlow PV",
    "photovoltaic_powerflow_load": "PV - PowerFlow Load",
    "photovoltaic_powerflow_grid": "SM - PowerFlow Grid",
    "photovoltaic_powerflow_battery": "PV - PowerFlow Battery",
    "battery_storage_command_mode": "B - Storage Command Mode",
    "battery_state_of_charge": "B - SOC",
    "battery_max_charge_power": "B - Max Charge Power",
    "battery_max_discharge_power": "B - Max Discharge Power",
    "heatpump_dhw_tank_temp": "HP - DHW Tank Temp",
    "heatpump_dhw_activated": "HP - DHW Activated",
    "heatpump_dhw_on_off": "HP - DHW on/off",
    "heatpump_heating_target_temp_normal": "HP - Heating Target Temp (normal)",
    "heatpump_heating_activated": "HP - Heating Activated",
    "heatpump_current_power_elect": "HP - Current Power (elect)",
    "heatpump_on_off": "HP - On/Off",
    "heatpump_temp_indoor_measured": "HP - Temp Indoor measured",
    "electronicvehicle_plugged": "EV - Plugged",
    "electronicvehicle_state_of_charge": "EV - SOC",
    "wallbox_current_charging_power": "WB - Current Charging Power"
}


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
        for key, value in LIST_OF_SENSORS.items():
            valueForSensor = loadSensorValueFor(key, value)
            if valueForSensor != "":
                sensorValues.append(json.dumps(valueForSensor))
        payload="";
        if len(sensorValues) > 0:
            sensorList = ",".join(sensorValues)
            payload = f"{{\"sensor_list\" : [{sensorList}]}}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SHYFT_ACCESS_KEY}"
            }
        #external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/obj/homeassistanttest"
        external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/wf/addon_sensor_data"
        response = requests.post(external_url, headers=headers, data=payload)
        status_code = response.status_code
        return jsonify({
            "status": "success",
            "payload": payload,
            "external_status": status_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


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


def loadEntityState(sensorId):
    response = getFromHA("/api/states/" + sensorId)
    unit = response.get("attributes", {}).get("unit_of_measurement", "")
    return {"state": response["state"],
            "unit" : unit}

def getFromHA(path):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}"
    }
    completeUri = HASSIO_URI + path
    response = requests.get(completeUri, headers=headers)
    return response.json()


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
            trigger()
        time.sleep(UPDATE_INTERVALL_IN_SECONDS)


thread = threading.Thread(target=callBubblePeriodically, daemon=True)
thread.start()

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
