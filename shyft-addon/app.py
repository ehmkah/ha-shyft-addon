import os
from flask import Flask, send_from_directory, jsonify, request
import requests
import json
import datetime
import shutil

app = Flask(__name__, static_folder="www", static_url_path="")
SHYFT_ACCESS_KEY = "not_set_yet"
OPTIONS_PATH = "/data/options.json"
CONFIG_PATH = "/data/config.json"
SUPERVISOR_TOKEN = value = os.getenv("SUPERVISOR_TOKEN")
HASSIO_URI_RUNNING_ON_HAOS = "http://supervisor/core"
HASSIO_URI_RUNNING_REMOTE = "http://homeassistant.local:8123"
HASSIO_URI = HASSIO_URI_RUNNING_ON_HAOS

# Serve the static HTML
@app.route("/")
def index():
    return send_from_directory("www", "index.html")

# Delivers data to bubble
@app.route("/trigger", methods=["POST"])
def trigger():
    try:
        valueForOne = loadEntityState("sensor.heatpump_mock_the_sensor_mock")

        headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {SHYFT_ACCESS_KEY}"
            }
        payload = "aTestValue=created+by+TimeSeriesResultsEntityRepositoryIntegrationTest.+can+be+Removed+without+problems&secondTestValue="+valueForOne
        external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/obj/homeassistanttest"

        response = requests.post(external_url, headers=headers, data=payload)
        return jsonify({"status": "success",
         "external_status": response.status_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/config", methods=["GET"])
def readConfig():
    content = "nothing"
    with open(CONFIG_PATH, "r") as file:
        print("Opened config file for reading")
        content = file.read()

    return content

@app.route("/config", methods=["PUT"])
def writeConfig():
    content = request.get_data(as_text=True)

    with open(CONFIG_PATH, "w") as file:
        print("Opened config file for writing")
        file.write(content)

    return content

def loadEntityState(sensorId):
    headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {SUPERVISOR_TOKEN}"
                }
    completeUri = HASSIO_URI+"/api/states/"+sensorId
    print("complete uri " +completeUri)
    response =  requests.get(completeUri, headers=headers)
    return response.json()["state"]


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
