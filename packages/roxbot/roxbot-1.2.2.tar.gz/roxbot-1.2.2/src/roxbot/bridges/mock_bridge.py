#!/usr/bin/env python3
"""
 Mock bridge, when no external interface is required.

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""
import asyncio
from .base import Bridge


class MockBridge(Bridge):
    """Mock bridge, when no external interface is required."""

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def send(self, topic: str, data):
        """send data to topic

        Args:
            topic (str): topic to post on
            data (any): json serializable data payload
        """

    async def serve(self):
        """just wait forever"""
        await asyncio.sleep(None)
