from homeassistant_adapter import HomeAssistantAdapter, PeriodElement

from datetime import datetime
from file_utils import read_file_to_json

import pytest

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

@pytest.mark.parametrize("given_input_file_name, expected_output_file_name", [
    ("shyft-addon/tests/data/entity_history_test_data_001.json", "shyft-addon/tests/data/expected_entity_history_test_data_001.json"),
    ("shyft-addon/tests/data/entity_history_test_data_002.json", "shyft-addon/tests/data/expected_entity_history_test_data_002.json"),
    ("shyft-addon/tests/data/entity_history_test_data_003.json", "shyft-addon/tests/data/expected_entity_history_test_data_003.json"),
])
def test_map_to_period_element(given_input_file_name:str, expected_output_file_name:str):
    # given
    sut = HomeAssistantAdapter(
        supervisor_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo")
    given_period_element = read_file_to_json(given_input_file_name)
    expected_periods = _read_to_period_element(expected_output_file_name)

    # WHEN
    actual = sut._map_to_period_element(given_period_element)


    ## THEN
    assert len(actual) == len(expected_periods)
    assert actual == expected_periods

@pytest.mark.parametrize("given_datetime, expected_datetime", [
    ("2025-12-06T20:31:00Z", "2025-12-06T20:20:00Z"),
    ("2025-12-06T20:31:00Z", "2025-12-06T20:20:00Z"),
    ("2025-12-06T20:31:00.1234Z", "2025-12-06T20:20:00Z"),
])
def test_datetime_to_bucket_time(given_datetime, expected_datetime):
    # given
    sut = HomeAssistantAdapter(supervisor_token="xxx")

    # when
    actual = sut._map_datetime_to_bucket_time(datetime.fromisoformat(given_datetime))

    # then
    assert actual == datetime.fromisoformat(expected_datetime)




def _read_to_period_element(file_path: str) -> PeriodElement:
    file_content = read_file_to_json(file_path)
    result: [PeriodElement] = []
    for entry in file_content:
        state = entry["state"]
        last_changed = datetime.fromisoformat(entry["last_changed"])
        result.append(PeriodElement(state, last_changed))

    return result



