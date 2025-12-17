from homeassistant_adapter import HomeAssistantAdapter
from shyft_adapter import ShyftAdapter
from constants import CONFIG_PATH

import json
import os

LIST_OF_SENSORS = {
    "photovoltaic_powerflow_pv": "PV - PowerFlow PV",
    "photovoltaic_powerflow_load": "PV - PowerFlow Load",
    "photovoltaic_powerflow_grid": "PV - PowerFlow Grid",
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

# does the mapping between homeassistant and shyft/ bubble
class SyncService:

    def __init__(self, homeassistantAdapter: HomeAssistantAdapter, shyftAdapter: ShyftAdapter, config_path: str = CONFIG_PATH):
        self.homeassistant_adapter = homeassistantAdapter
        self.shyft_adapter = shyftAdapter
        self.config_path = config_path

    def sync_pv_history(self):
        pass
        #try:
        #    LIST_OF_SENSORS

            #for key, value in LIST_OF_SENSORS.items():
            #    valueForSensor = loadSensorValueFor(key, value)
            #    if valueForSensor != "":
#                    sensorValues.append(json.dumps(valueForSensor))
#            payload = ""
#            if len(sensorValues) > 0:
#                sensorList = ",".join(sensorValues)
#                payload = f"{{\"sensor_list\" : [{sensorList}]}}"
#                headers = {
#                    "Content-Type": "application/json",
#                    "Authorization": f"Bearer {SHYFT_ACCESS_KEY}"
#                }
#            # external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/obj/homeassistanttest"
#            external_url = "https://anselmhuewe.bubbleapps.io/version-test/api/1.1/wf/addon_pv_history"
#            response = requests.post(external_url, headers=headers, data=payload)
#            status_code = response.status_code
#            return jsonify({
#                "status": "success",
#                "payload": payload,
#                "external_status": status_code})
#        except Exception as e:
#            return jsonify({"status": "error", "message": str(e)})
#
#
    def _load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            return json.load(file)
