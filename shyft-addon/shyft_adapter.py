import json

from constants import BUBBLE_URI, BUBBLE_TOKEN
from homeassistant_adapter import PeriodElement

import requests

# Communicates with shyft on bubble
class ShyftAdapter:

    def __init__(self,
                 bubble_uri=BUBBLE_URI,
                 bubble_token=BUBBLE_TOKEN):
        self.bubble_uri = bubble_uri
        self.bubble_token = bubble_token

    def send_pv_history(self,
                        pv_history: [PeriodElement]):
        payload = self._map_to_json(pv_history)

        return self._call_workflow("addon_pv_history", payload)

    def _call_workflow(self,
                       workflow_name: str,
                       payload: str):
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.bubble_token}"
            }
            complete_uri = f"{self.bubble_uri}api/1.1/wf/{workflow_name}"
            response = requests.post(complete_uri, headers=headers, data=payload)
            status_code = response.status_code
            return json.dumps({
                "status": "success",
                "payload": payload,
                "external_status": status_code})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def _map_to_json(self, pv_history: [PeriodElement]):
        list_of_values = []
        for one_history_element in pv_history:
            list_of_values.append({"state": one_history_element.state,
                                   "last_changed": one_history_element.last_changed.isoformat()})
        return json.dumps({"pv_history_list": list_of_values})
