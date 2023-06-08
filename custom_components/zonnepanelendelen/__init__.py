"""Zonnepanelendelen integration"""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .const import PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup(
    hass: HomeAssistant,
    config: ConfigType,
) -> bool:
    """Setup ZPD integration"""

    _LOGGER.debug("async_setup called")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Load the saved entities."""

    _LOGGER.debug("async_setup_entry called")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    _LOGGER.debug("async_unload_entry called")

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
