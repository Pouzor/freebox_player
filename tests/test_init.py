"""Tests for the Freebox Player setup and remote service."""

from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.freebox_player.const import (
    CONF_REMOTE_CODE,
    DOMAIN,
    SERVICE_REMOTE,
)

ENTRY_DATA = {CONF_HOST: "192.168.0.10", CONF_REMOTE_CODE: "12345678"}
BASE_URL = "http://192.168.0.10/pub/remote_control"


async def _setup_entry(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN, data=ENTRY_DATA, unique_id=ENTRY_DATA[CONF_HOST])
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_setup_registers_service(hass: HomeAssistant) -> None:
    """Setting up an entry registers the remote service."""
    await _setup_entry(hass)
    assert hass.services.has_service(DOMAIN, SERVICE_REMOTE)


async def test_unload_removes_service(hass: HomeAssistant) -> None:
    """Unloading the entry removes the remote service."""
    entry = await _setup_entry(hass)
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert not hass.services.has_service(DOMAIN, SERVICE_REMOTE)


async def test_remote_service_sends_single_code(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Calling the service sends one request with the right params."""
    aioclient_mock.get(BASE_URL, text="")
    await _setup_entry(hass)

    await hass.services.async_call(DOMAIN, SERVICE_REMOTE, {"code": "power"}, blocking=True)

    assert len(aioclient_mock.mock_calls) == 1
    _, url, _, _ = aioclient_mock.mock_calls[0]
    assert url.query["code"] == "12345678"
    assert url.query["key"] == "power"


async def test_remote_service_splits_codes(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Comma-separated codes produce one request per code."""
    aioclient_mock.get(BASE_URL, text="")
    await _setup_entry(hass)

    await hass.services.async_call(DOMAIN, SERVICE_REMOTE, {"code": "1, 2 ,3"}, blocking=True)

    assert len(aioclient_mock.mock_calls) == 3
    keys = [call[1].query["key"] for call in aioclient_mock.mock_calls]
    assert keys == ["1", "2", "3"]


async def test_remote_service_handles_http_error(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """A failing request is swallowed (logged, not raised)."""
    aioclient_mock.get(BASE_URL, status=500)
    await _setup_entry(hass)

    # Should not raise despite the 500 response.
    await hass.services.async_call(DOMAIN, SERVICE_REMOTE, {"code": "power"}, blocking=True)
    assert len(aioclient_mock.mock_calls) == 1
