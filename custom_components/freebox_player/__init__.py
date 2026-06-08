"""Freebox Player remote control integration.

https://github.com/Pouzor/freebox_player
"""

from __future__ import annotations

import logging

import aiohttp
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .const import CONF_REMOTE_CODE, DOMAIN, REMOTE_PATH, SERVICE_REMOTE

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_REMOTE_CODE): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

SERVICE_REMOTE_SCHEMA = vol.Schema({vol.Required("code"): cv.string})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration from YAML by importing into a config entry.

    YAML configuration is deprecated; this only migrates an existing
    `configuration.yaml` block into a UI config entry once.
    """
    conf = config.get(DOMAIN)
    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
            )
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Freebox Player from a config entry."""
    host: str = entry.data[CONF_HOST]
    remote_code: str = entry.data[CONF_REMOTE_CODE]
    base_url = f"http://{host}{REMOTE_PATH}"
    session = async_get_clientsession(hass)

    async def async_handle_remote(call: ServiceCall) -> None:
        """Send one or more remote key codes to the player.

        Codes are comma-separated to emulate a sequence (e.g. "1,2,3").
        """
        codes = [code.strip() for code in call.data["code"].split(",") if code.strip()]
        for code in codes:
            try:
                async with session.get(
                    base_url, params={"code": remote_code, "key": code}
                ) as response:
                    response.raise_for_status()
            except aiohttp.ClientError as err:
                _LOGGER.error("Failed to send remote code '%s': %s", code, err)

    hass.services.async_register(
        DOMAIN, SERVICE_REMOTE, async_handle_remote, schema=SERVICE_REMOTE_SCHEMA
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and remove the registered service."""
    hass.services.async_remove(DOMAIN, SERVICE_REMOTE)
    return True
