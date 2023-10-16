#!/usr/bin/env python3
"""
 Base classes for Hardware Abstraction Layer (HAL) components.
 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import asyncio
import logging
from enum import Enum
from typing import List, Optional

from roxbot.bridges.base import Bridge
from roxbot.bridges.mock_bridge import MockBridge
from roxbot.topics import Topics


# device types
class DeviceType(Enum):
    """Device types"""

    SERVO = 1
    REMOTE_IO = 2
    E_STOP = 3
    OTHER = 4


class Device:
    """Base class for hardware devices. It is used to define the interfaces and behavior"""

    def __init__(
        self, name: str, device_type: DeviceType, bridge: Optional[Bridge] = None
    ) -> None:
        """Base class for hardware devices

        Args:
            name (str): Device name to be used in logs etc.
            device_type (DeviceType): device class
            bridge (Bridge): External interface. Defaults to MockBridge() instance.
        """
        self.name = name

        if bridge is None:
            bridge = MockBridge()

        self.bridge: Bridge = bridge

        self.device_type = device_type

        self._topics = Topics(self.name)

        self._log = logging.getLogger(f"{self.name}")

        self._connected = False

        # coroutine list, append new coroutines here
        self._coros: List = [self._heartbeat]

    def get_errors(self) -> List:
        """get list of errors from device"""
        return []

    def clear_errors(self):
        """clear errors from device"""

    async def main(self):
        """main coroutine"""
        async with asyncio.TaskGroup() as tg:
            for coro in self._coros:
                self._log.debug("starting %s", coro.__name__)
                tg.create_task(coro())

    def run(self):
        """run device coroutines"""
        asyncio.run(self.main())

    # ---------- async coroutines ------------
    async def _heartbeat(self):
        """publish heartbeat to bridge"""

        idx = 0

        while True:
            data = {"name": self.name, "idx": idx}
            self.bridge.send(self._topics.heartbeat, data)
            idx += 1
            await asyncio.sleep(1)

    def __str__(self) -> str:
        return f"{self.device_type.name} {self.name}"
