"""Freebox Player remote control integration.

https://github.com/Pouzor/freebox_player
"""

from __future__ import annotations

import logging

import aiohttp
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

DOMAIN = "freebox_player"
CONF_REMOTE_CODE = "remote_code"
REMOTE_PATH = "/pub/remote_control"
SERVICE_REMOTE = "remote"

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
    """Set up the Freebox Player component from YAML configuration."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    host: str = conf[CONF_HOST]
    remote_code: str = conf[CONF_REMOTE_CODE]
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
