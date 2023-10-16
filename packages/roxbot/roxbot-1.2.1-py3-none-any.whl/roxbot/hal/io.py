#!/usr/bin/env python3
"""
 IO device definitions

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
from enum import Enum
from typing import Optional, List

from roxbot.bridges.base import Bridge

from .base import Device, DeviceType


class InputDirection(Enum):
    """Input direction"""

    UNDEFINED = 0
    INPUT = 1
    OUTPUT = 2


class DigitalIO:
    """Digital IO"""

    def __init__(self, direction: InputDirection) -> None:
        self._direction = direction
        self.value: bool = False

    def set(self, value: bool):
        """set value"""
        assert self._direction == InputDirection.OUTPUT, "can't set value on input"
        self.value = value

    def __repr__(self) -> str:
        return "1" if self.value else "0"


class AnalogIO:
    """Analog IO"""

    def __init__(self, direction: InputDirection) -> None:
        self._direction = direction
        self.value: float = 0.0

    def set(self, value: float):
        """set value"""
        assert self._direction == InputDirection.OUTPUT, "can't set value on input"
        self.value = value


class RemoteIO(Device):
    """Remote IO device"""

    def __init__(self, name: str, bridge: Optional[Bridge] = None) -> None:
        super().__init__(name, DeviceType.REMOTE_IO, bridge)

        self.dio: List[DigitalIO] = []  # digital inputs/outputs
        self.aio: List[AnalogIO] = []  # analog inputs/outputs
