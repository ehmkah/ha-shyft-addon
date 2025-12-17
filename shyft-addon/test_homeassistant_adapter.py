from homeassistant_adapter import HomeAssistantAdapter, PeriodElement

from datetime import datetime

def test_load_entity_history():
    sut = HomeAssistantAdapter()
    actual: [PeriodElement] = sut.load_entity_history("sensor.heatpump_mock_the_sensor_mock",
                                                      datetime.fromisoformat("2025-12-06T20:31:00"),
                                                      datetime.fromisoformat("2025-12-31T21:31:00"))
    assert len(actual) == 1
    assert actual[0].state == "10"
    assert actual[0].last_changed == "2025-12-06T19:31:00+00:00"

def test_load_entity_status():
    sut = HomeAssistantAdapter()
    actual = sut.load_entity_state("sensor.heatpump_mock_the_sensor_mock")
    assert actual["state"] == "10"
    assert actual["unit"] == "°C"

