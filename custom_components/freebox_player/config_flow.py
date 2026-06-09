"""Config flow for the Freebox Player integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST

from .const import CONF_REMOTE_CODE, DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_REMOTE_CODE): str,
    }
)


class FreeboxPlayerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Freebox Player."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the user-initiated setup step."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

    async def async_step_import(self, import_data: dict[str, Any]) -> ConfigFlowResult:
        """Import configuration from configuration.yaml (deprecated)."""
        await self.async_set_unique_id(import_data[CONF_HOST])
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=import_data[CONF_HOST], data=import_data)
