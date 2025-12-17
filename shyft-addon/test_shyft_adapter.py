from shyft_adapter import ShyftAdapter
from homeassistant_adapter import PeriodElement

from datetime import datetime
import json

def test_send_pv_history():
    expected = json.dumps({"pv_history_list":[{"state": "10","last_changed": datetime.fromisoformat("2025-05-21T18:00:00Z").isoformat()}]})
    sut = ShyftAdapter()
    given_pv_history = [PeriodElement("10", datetime.fromisoformat("2025-05-21T18:00:00Z"))]
    actual = sut._map_to_json(given_pv_history)

    assert expected == actual