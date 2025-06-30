
metadata = {
    "apiLevel": "2.11"
}

from opentrons import protocol_api
from opentrons.drivers.smoothie_drivers.driver_3_0 import SmoothieDriver


def run(protocol: protocol_api.ProtocolContext):
	protocol.comment("B and C motors are performing the unstick axes commands")
	if not protocol.is_simulating:
		for i in range(3):
				protocol._hw_manager.hardware._backend._smoothie_driver.unstick_axes('BC')
