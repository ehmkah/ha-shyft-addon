from sync_service import SyncService
from homeassistant_adapter import HomeAssistantAdapter
from shyft_adapter import ShyftAdapter

import pytest

@pytest.fixture
def sut():
    return SyncService(HomeAssistantAdapter(),
                       ShyftAdapter(bubble_token="XXXX"),
                       "shyft-addon/test_shyft_config.json")

def test_trigger_pv_history(sut):
    sut.sync_pv_history()

def test_load_config(sut):
    actual = sut._load_config()
    assert actual["sensorMappings"]["photovoltaic_powerflow_pv"] == "sensor.heatpump_mock_the_sensor_mock"
