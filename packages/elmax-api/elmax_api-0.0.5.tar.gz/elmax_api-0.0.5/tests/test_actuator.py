"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.model.command import SwitchCommand
from elmax_api.model.panel import PanelStatus, PanelEntry
from tests import client, LOCAL_TEST


def setup_module(module):

    if not LOCAL_TEST:
        panels = asyncio.run(client.list_control_panels())
        online_panels = list(filter(lambda x: x.online, panels))
        assert len(online_panels) > 0

        # Select the first online panel
        entry = online_panels[0]  # type:PanelEntry
        client.set_current_panel(panel_id=entry.hash)


@pytest.mark.asyncio
async def test_device_command():
    # Retrieve its status
    panel = await client.get_current_panel_status()  # type: PanelStatus
    assert isinstance(panel, PanelStatus)

    # Store old status into a dictionary for later comparison
    expected_actuator_status = { actuator.endpoint_id:actuator.opened for actuator in panel.actuators}

    # Toggle the first 3 actuators actuators
    actuators = list(expected_actuator_status.items())[:min(len(expected_actuator_status.items()),3)]

    tasks = []
    for endpoint_id, curr_status in actuators:
        command = SwitchCommand.TURN_OFF if curr_status else SwitchCommand.TURN_ON
        print(f"Actuator {endpoint_id} was {curr_status}, issuing {command}...")
        tasks.append(client.execute_command(endpoint_id=endpoint_id, command=command))
        # Set actuator expected status
        expected_actuator_status[endpoint_id] = not curr_status
    await asyncio.gather(*tasks)

    # Ensure all the actuators switched correctly
    await asyncio.sleep(3)
    panel = await client.get_current_panel_status()  # type: PanelStatus

    for actuator in panel.actuators:
        expected_status = expected_actuator_status[actuator.endpoint_id]
        print(f"Actuator {actuator.endpoint_id} expected {expected_status}, was {actuator.opened}...")
        assert actuator.opened == expected_status
