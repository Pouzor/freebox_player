"""Tests for the Freebox Player config flow."""

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.freebox_player.const import CONF_REMOTE_CODE, DOMAIN

USER_INPUT = {CONF_HOST: "192.168.0.10", CONF_REMOTE_CODE: "12345678"}


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """A user-initiated flow creates a config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(result["flow_id"], USER_INPUT)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "192.168.0.10"
    assert result["data"] == USER_INPUT


async def test_user_flow_aborts_if_already_configured(hass: HomeAssistant) -> None:
    """A second entry for the same host is aborted."""
    MockConfigEntry(domain=DOMAIN, data=USER_INPUT, unique_id=USER_INPUT[CONF_HOST]).add_to_hass(
        hass
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(result["flow_id"], USER_INPUT)
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_import_flow_creates_entry(hass: HomeAssistant) -> None:
    """YAML import creates a config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=USER_INPUT
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == USER_INPUT


async def test_import_flow_aborts_duplicate(hass: HomeAssistant) -> None:
    """Re-importing the same host is aborted."""
    MockConfigEntry(domain=DOMAIN, data=USER_INPUT, unique_id=USER_INPUT[CONF_HOST]).add_to_hass(
        hass
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=USER_INPUT
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
