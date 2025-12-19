from sync_service import SyncService
from homeassistant_adapter import HomeAssistantAdapter
from shyft_adapter import ShyftAdapter

import pytest

@pytest.fixture
def sut():
    return SyncService(HomeAssistantAdapter(supervisor_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo"),
                       ShyftAdapter(bubble_token="XXXX"),
                       "shyft-addon/test_shyft_config.json")

def test_sync_pv_history(sut):
    sut.sync_pv_history()

def test_sync_all_sensors(sut):
    sut.sync_all_sensors()

def test_load_config(sut):
    actual = sut._load_config()
    assert actual["sensorMappings"]["photovoltaic_powerflow_pv"] == "sensor.heatpump_mock_the_sensor_mock"
