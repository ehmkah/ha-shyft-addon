from homeassistant_adapter import HomeAssistantAdapter

def test_load_entity_history():
    sut = HomeAssistantAdapter("http://homeassistant.local:8123", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlOGQyNjEwZmMwOWQ0MzY3OTQ5YzcyZDc4ZjA2MzliMyIsImlhdCI6MTc2MDA5Njc2NiwiZXhwIjoyMDc1NDU2NzY2fQ.uzrb_9GI--oKn6Wt6Oopz-lweUWXV0Q4ABbwxmAiiJo")
    actual = sut.load_entity_history("sensor.heatpump_mock_the_sensor_mock", "2025-12-06T20:31:00", "2025-12-31T21:31:00")
    assert len(actual) == 1
    assert actual[0].state == "10"