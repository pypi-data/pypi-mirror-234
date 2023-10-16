"""Test control panel functionalities."""
import asyncio

import pytest

from elmax_api.constants import DEFAULT_PANEL_PIN
from elmax_api.exceptions import ElmaxBadPinError
from elmax_api.model.actuator import Actuator
from elmax_api.model.area import Area
from elmax_api.model.cover import Cover
from elmax_api.model.goup import Group
from elmax_api.model.panel import PanelStatus
from elmax_api.model.scene import Scene
from elmax_api.model.zone import Zone
from tests import client, LOCAL_TEST


def setup_module(module):
    if not LOCAL_TEST:
        panels = asyncio.run(client.list_control_panels())
        online_panels = list(filter(lambda x: x.online, panels))
        assert len(online_panels) > 0

        # Select the first online panel
        entry = online_panels[0]
        client.set_current_panel(panel_id=entry.hash)


@pytest.mark.asyncio
async def test_list_control_panels():
    if LOCAL_TEST:
        pytest.skip("Skipping test_list_control_panels as testing local API")
        return
    panels = await client.list_control_panels()
    assert len(panels) > 0


@pytest.mark.asyncio
async def test_get_control_panel_status():
    # Retrieve its status
    status = await client.get_current_panel_status()  # type: PanelStatus
    assert isinstance(status, PanelStatus)

    # Make sure the username matches the one used by the client
    # TODO: parametrize the following check
    #assert status.user_email == USERNAME


@pytest.mark.asyncio
async def test_wrong_pin():
    if LOCAL_TEST:
        pytest.skip("Skipping bad pin test for LOCAL API tests")
    panels = await client.list_control_panels()
    online_panels = list(filter(lambda x: x.online, panels))
    assert len(online_panels) > 0

    # Select the first panel
    panel = online_panels[0]

    # Retrieve its status
    with pytest.raises(ElmaxBadPinError):
        client.set_current_panel(panel.hash, "111111")
        # This will trigger the exception
        await client.get_current_panel_status()  # type: PanelStatus

    # Make sure to re-set the original panel pin
    client.set_current_panel(panel.hash, DEFAULT_PANEL_PIN)

@pytest.mark.asyncio
async def test_single_device_status():
    # Retrieve its status
    status = await client.get_current_panel_status()  # type: PanelStatus
    assert isinstance(status, PanelStatus)

    # Make sure we can read each status correctly
    for endpoint in status.all_endpoints:
        epstatus = await client.get_endpoint_status(endpoint_id=endpoint.endpoint_id)

        if isinstance(endpoint, Actuator):
            assert epstatus.actuators[0] == endpoint
        elif isinstance(endpoint, Area):
            assert epstatus.areas[0] == endpoint
        elif isinstance(endpoint, Group):
            assert epstatus.groups[0] == endpoint
        elif isinstance(endpoint, Scene):
            assert epstatus.scenes[0] == endpoint
        elif isinstance(endpoint, Zone):
            assert epstatus.zones[0] == endpoint
        elif isinstance(endpoint, Cover):
            assert epstatus.covers[0] == endpoint
        else:
            raise ValueError("Unexpected/unhandled endpoint")
