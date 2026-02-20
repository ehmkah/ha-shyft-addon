from homeassistant_adapter import HomeAssistantAdapter, PeriodElement

from datetime import datetime
from file_utils import read_file_to_json

def test_load_entity_history():
    sut = HomeAssistantAdapter(supervisor_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo")
    actual: [PeriodElement] = sut.load_entity_history("sensor.heatpump_mock_the_sensor_mock",
                                                      datetime.fromisoformat("2025-12-06T20:31:00"),
                                                      datetime.fromisoformat("2025-12-31T21:31:00"))
    assert len(actual) == 1
    assert actual[0].state == "10"
    assert actual[0].last_changed == "2025-12-06T19:31:00+00:00"

def test_load_entity_status():
    sut = HomeAssistantAdapter(supervisor_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo")
    actual = sut.load_entity_state("sensor.heatpump_mock_the_sensor_mock")
    assert actual.state == "10"
    assert actual.unit == "°C"

def test_map_to_period_element():
    # given
    sut = HomeAssistantAdapter(
        supervisor_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo")
    given_period_element = read_file_to_json("shyft-addon/tests/data/entity_history_test_data_001.json")
    expected_periods = _read_to_period_element("shyft-addon/tests/data/expected_entity_history_test_data_001.json")

    # WHEN
    actual = sut._map_to_period_element(given_period_element)


    ## THEN
    assert actual == expected_periods


def _read_to_period_element(file_path: str) -> PeriodElement:
    file_content = read_file_to_json(file_path)
    result: [PeriodElement] = []
    for entry in file_content:
        state = entry["state"]
        last_changed = datetime.fromisoformat(entry["last_changed"])
        result.append(PeriodElement(state, last_changed))

    return result


