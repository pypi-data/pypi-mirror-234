#!/usr/bin/env python3
"""
 HAL for  CAONpen devices. Work in progress.

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
from typing import Optional, List

import asyncio
import logging
from roxbot.bridges.base import Bridge
from .base import Device
from .io import RemoteIO, DigitalIO, InputDirection


class CanBus_Mock:
    """interface to CAN bus"""

    def __init__(
        self, bridge: Optional[Bridge] = None, interface: str = "vcan0"
    ) -> None:
        """Create mock CANopen bus with a couple of attached devices

        Args:
            bridge (Optional[Bridge], optional): bridge interface to other systems. Defaults to None.
            interface (str, optional): CANopen interface name. Defaults to "vcan0".
        """
        self._log = logging.getLogger(f"{self.__class__.__name__}")
        self._bridge = bridge
        self._interface = interface
        self._connected = False
        self.devices: List[Device] = []

    async def main(self):
        """main coroutine"""
        self._log.info("starting CAN bus on %s", self._interface)

        self.devices = [
            RemoteIO_Mock("io1", self._bridge),
            RemoteIO_Mock("io2", self._bridge),
        ]

        # start system
        async with asyncio.TaskGroup() as tg:
            for dev in self.devices:
                tg.create_task(dev.main())

    async def start(self):
        """start CAN bus"""
        asyncio.create_task(self.main())
        await asyncio.sleep(0.01)


class RemoteIO_Mock(RemoteIO):
    """simulated remote IO device with 8 digital inputs"""

    def __init__(self, name: str, bridge=None) -> None:
        super().__init__(name, bridge)

        for _ in range(8):
            self.dio.append(DigitalIO(InputDirection.INPUT))

        self._coros.append(self._simulate_io)

    async def _simulate_io(self):
        """simulate IO as a binary counter"""
        counter = 0
        while True:
            self._log.debug("counter: %s", counter)
            await asyncio.sleep(1)

            # Update the dio values based on the binary representation of the counter
            for i, dio in enumerate(self.dio):
                dio.value = (counter & (1 << i)) != 0

            # Increment the counter and wrap it if it reaches 256 (for 8 bits)
            counter = (counter + 1) % 256
