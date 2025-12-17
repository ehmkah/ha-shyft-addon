import requests


class PeriodElement:
    def __init__(self, state, unit_of_measurement, timestamp):
        self.state = state
        self.unit_of_measurement = unit_of_measurement
        self.timestamp = timestamp


# Adapter for integrating homeassistant
class HomeAssistantAdapter:

    def __init__(self, homeAssistantUri, supervisorToken):
        self.homeAssistantUri = homeAssistantUri
        self.supervisorToken = supervisorToken

    def loadEntityState(self, sensor_id):
        response = self._getFromHA("/api/states/" + sensor_id)
        unit = response.get("attributes", {}).get("unit_of_measurement", "")
        return {"state": response["state"],
                "unit": unit}

    def load_entity_history(self, sensor_id, start_timestamp, end_timestamp):
        response = self._getFromHA(
            "/api/history/period/" + start_timestamp + "?end_time=" + end_timestamp + "&filter_entity_id=" + sensor_id + "&minimal_response")
        result = []
        for response_entry in response:
            for one_period in response_entry:
                unit = one_period.get("attributes", {}).get("unit_of_measurement", "")
                state = one_period["state"]
                last_changed = one_period["last_changed"]
                result.append(PeriodElement(state, unit, last_changed))

        return result

    def _getFromHA(self, path):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.supervisorToken}"
        }
        completeUri = self.homeAssistantUri + path
        response = requests.get(completeUri, headers=headers)
        return response.json()
