from constants import HOMEASSISTANT_SUPERVISOR_TOKEN, HOMEASSISTANT_URI

from datetime import datetime
import requests


class PeriodElement:
    def __init__(self, state: str, last_changed: datetime):
        self.state = state
        self.last_changed = last_changed


class EntityState:
    def __init__(self, state: str, unit: str):
        self.state = state
        self.unit = unit


# Adapter for integrating homeassistant
class HomeAssistantAdapter:

    def __init__(self,
                 homeassistant_uri: str = HOMEASSISTANT_URI,
                 supervisor_token: str = HOMEASSISTANT_SUPERVISOR_TOKEN):
        self.homeassistant_uri = homeassistant_uri
        self.supervisor_token = supervisor_token

    def load_entity_state(self,
                          sensor_id: str) -> EntityState:

        response = self._getFromHA("/api/states/" + sensor_id)
        unit = response.get("attributes", {}).get("unit_of_measurement", "")

        return EntityState(response["state"], unit)


def load_entity_history(self, sensor_id: str,
                        start_timestamp: datetime,
                        end_timestamp: datetime) -> [PeriodElement]:
    response = self._getFromHA(
        "/api/history/period/" + start_timestamp.isoformat() + "?end_time=" + end_timestamp.isoformat() + "&filter_entity_id=" + sensor_id + "&minimal_response")
    result : [PeriodElement] = []
    for response_entry in response:
        for one_period in response_entry:
            state = one_period["state"]
            last_changed = datetime.fromisoformat(one_period["last_changed"])
            result.append(PeriodElement(state, last_changed))

    return result


def _getFromHA(self, path):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {self.supervisor_token}"
    }
    completeUri = self.homeassistant_uri + path
    response = requests.get(completeUri, headers=headers)
    return response.json()
