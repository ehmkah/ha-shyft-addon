import os
from flask import Flask, send_from_directory, jsonify
import requests
import json

app = Flask(__name__, static_folder="www", static_url_path="")
SHYFT_ACCESS_KEY = "not_set_yet"
OPTIONS_PATH = "/data/options.json"

# Serve the static HTML
@app.route("/")
def index():
    return send_from_directory("www", "index.html")

# Endpoint called when the button is clicked
@app.route("/trigger", methods=["POST"])
def trigger():
    try:
        headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Bearer {SHYFT_ACCESS_KEY}"
            }
        payload = "aTestValue=created+by+TimeSeriesResultsEntityRepositoryIntegrationTest.+can+be+Removed+without+problems"
        external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/obj/homeassistanttest"

        response = requests.post(external_url, headers=headers, data=payload)
        return jsonify({"status": "success",
         "external_status": response.status_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/config", methods=["GET"])
def readConfig():
    return jsonify({"ausjelesen": "ausgelesen"})

if __name__ == "__main__":
    try:
        with open(OPTIONS_PATH, "r") as f:
            options = json.load(f)
            SHYFT_ACCESS_KEY = options.get("shyft_access_key", SHYFT_ACCESS_KEY)
    except Exception as e:
        print("Failed to load config from options.json:", e)

    print("✅ Loaded SHYFT_ACCESS_KEY:", SHYFT_ACCESS_KEY)
    app.run(host="0.0.0.0", port=8080)