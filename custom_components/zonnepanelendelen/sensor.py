"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .api import API
from .const import PROJECTS_KEY
from . import _LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    _LOGGER.debug("async_setup_entry called")

    config = config_entry.data

    # check if component was configured properly
    if CONF_USERNAME not in config or CONF_PASSWORD not in config:
        _LOGGER.debug("compontent not configured")

        return

    # login to API
    zpd_client = API(config[CONF_USERNAME], config[CONF_PASSWORD])
    await hass.async_add_executor_job(zpd_client.login)

    # get list of projects invested in
    projects = await hass.async_add_executor_job(zpd_client.projects)
    # create sensors per project
    sensors = []
    for project in projects[PROJECTS_KEY]:
        sensor = ZPDProject(
            api=zpd_client, project_id=project["id"], project_name=project["name"]
        )
        sensor.api = zpd_client
        sensor.project_id = project["id"]
        sensors.append(sensor)
        _LOGGER.debug("adding sensor for project %d", project["id"])

    async_add_entities(sensors)


class ZPDProject(SensorEntity):
    """Zonnepanelendelen project sensor"""

    api: API
    project_id: int

    _attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
    _attr_native_value = 0
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:solar-panel-large"

    def __init__(self, api: API, project_id: int, project_name: str) -> None:
        self.api = api
        self.project_id = project_id
        self._attr_name = f"{project_name}"
        self._attr_unique_id = f"zpd_project_{project_id}"

    async def async_update(self) -> None:
        """Fetch latest production data for this project"""

        _LOGGER.debug("async_update called for project %d", self.project_id)

        data = await self.hass.async_add_executor_job(self.api.project, self.project_id)
        self._attr_native_value = data["metrics"]["production_all"]["total_power_kWh"]
