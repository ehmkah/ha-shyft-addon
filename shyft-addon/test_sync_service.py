from sync_service import SyncService
from homeassistant_adapter import HomeAssistantAdapter
from shyft_adapter import ShyftAdapter


def test_trigger_pv_history():
    sut = SyncService(HomeAssistantAdapter(), ShyftAdapter())


def test_load_config():
    sut = SyncService(HomeAssistantAdapter(), ShyftAdapter(), "shyft-addon/test_shyft_config.json")
    actual = sut._load_config()
    assert actual["sensorMappings"]["photovoltaic_powerflow_pv"] == "sensor.heatpump_mock_the_sensor_mock"
