"""
Freebox Player Controller
https://github.com/Pouzor/freebox_player
"""

import logging
import requests
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.const import CONF_HOST, EVENT_HOMEASSISTANT_STOP

DOMAIN = "freebox_player"
player_path = "/pub/remote_control"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Required(CONF_HOST): cv.string, vol.Required("remote_code"): cv.string}
        )
    },
    extra=vol.ALLOW_EXTRA,
)

REMOTE_SCHEMA = vol.Schema(
    {
        vol.Optional("code"): cv.string
    }
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Freebox player component."""
    conf = config.get(DOMAIN)

    if conf is not None:
        host = conf.get(CONF_HOST)
        remote_code = conf.get("remote_code")
        global player_path
        player_path = "http://"+host+player_path+"?code="+remote_code+"&key="

        await async_setup_freebox_player(hass, config, host, remote_code)

    return True

async def async_setup_freebox_player(hass, config, host, port):

    async def async_freebox_player_remote(call):
        """Handle old player control (remote emulation)"""

        code_list = call.data.get('code')

        code_array = code.split(',')

        """Handle multiple codes, separated by comma"""
        for code in code_array:
            requests.get(player_path+code, verify=False)

    hass.services.async_register(DOMAIN, "remote", async_freebox_player_remote)
