from constants import HOMEASSISTANT_URI

from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

class PeriodElement:
    def __init__(self, state: str, last_changed: datetime):
        self.state = state
        self.last_changed = last_changed

    def __eq__(self, other):
        if not isinstance(other, PeriodElement):
            return False

        return self.state == other.state and self.last_changed == other.last_changed


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
        self.detailed_logging = False

    def load_entity_state(self,
                          sensor_id: str):

        query = "/api/states/" + sensor_id
        self._log_info("load_entity_state query " + query)
        response = self.get_from_homeassistant(query)
        unit = response.get("attributes", {}).get("unit_of_measurement", "")
        self._log_info("load_entity_state result " + str(response))
        return EntityState(response["state"], unit)

    def load_entity_history(self, sensor_id: str,
                            start_timestamp: datetime,
                            end_timestamp: datetime) -> [PeriodElement]:
        query = "/api/history/period/" + start_timestamp.isoformat() + "?end_time=" + end_timestamp.isoformat() + "&filter_entity_id=" + sensor_id + "&minimal_response"
        self._log_info("load_entity_history query " + query)
        response = self.get_from_homeassistant(query)
        self._log_info("load_entity_history result " + str(response))
        result = self._map_to_period_element(response)

        return result

    def _log_info(self, log_message: str):
        if self.detailed_logging:
            logger.info(log_message)

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
