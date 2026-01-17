from constants import HOMEASSISTANT_URI

from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

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
                 supervisor_token: str,
                 homeassistant_uri: str = HOMEASSISTANT_URI):
        self.homeassistant_uri = homeassistant_uri
        self.supervisor_token = supervisor_token

    def load_entity_state(self,
                          sensor_id: str):

        response = self.get_from_homeassistant("/api/states/" + sensor_id)
        unit = response.get("attributes", {}).get("unit_of_measurement", "")
        logger.info("load_entity_state")

        return EntityState(response["state"], unit)


    def load_entity_history(self, sensor_id: str,
                            start_timestamp: datetime,
                            end_timestamp: datetime) -> [PeriodElement]:
        response = self.get_from_homeassistant(
            "/api/history/period/" + start_timestamp.isoformat() + "?end_time=" + end_timestamp.isoformat() + "&filter_entity_id=" + sensor_id + "&minimal_response")
        result = self._map_to_period_element(response)

        return result

    def _map_to_period_element(self, response) -> [PeriodElement]:
        result: [PeriodElement] = []
        for response_entry in response:
            for one_period in response_entry:
                state = one_period["state"]
                last_changed = datetime.fromisoformat(one_period["last_changed"])
                result.append(PeriodElement(state, last_changed))
        return result

    def get_from_homeassistant(self, path):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.supervisor_token}"
        }
        completeUri = self.homeassistant_uri + path
        response = requests.get(completeUri, headers=headers)
        try:
            return response.json()
        except:
            raise Exception(response.text)

