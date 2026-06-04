from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from . import utils

PLATFORMS = (Platform.MEDIA_PLAYER, Platform.STT)


async def async_setup(hass: HomeAssistant, hass_config: dict) -> bool:
    return await hass.async_add_executor_job(utils.install)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    config_entry.runtime_data = await hass.async_add_executor_job(
        utils.Model, hass, config_entry.data
    )
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
