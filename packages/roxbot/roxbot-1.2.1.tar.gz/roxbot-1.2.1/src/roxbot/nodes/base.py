#!/usr/bin/env python3
"""
 Base classes for node system

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

from abc import ABC, abstractmethod
from typing import List, Callable, Awaitable, Set, Dict, Union, Optional
import asyncio
import logging

# simpify type hinting
InputsType = Dict[str, Union[Callable, asyncio.Queue]]
OutputsType = Dict[str, Union["CallbackOutput", "QueueOutput"]]
CorosListType = List[Callable[[], Awaitable[None]]]


class Node(ABC):
    """system node class"""

    def __init__(self, name: str) -> None:
        self.name = name

        # logger
        self.log = logging.getLogger(name)

        # inputs and outputs
        self.inputs: InputsType = {}
        self.outputs: OutputsType = {}

    @abstractmethod
    async def main(self):
        """main coroutine"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class CallbackOutput:
    """Output class for nodes, calls a callback when data is received.
    CallbackOutput supports multiple connected inputs"""

    def __init__(self) -> None:
        self._callbacks: Set[Callable] = set()

    def connect(self, fcn: Callable):
        """connect some input by registering callback"""
        self._callbacks.add(fcn)

    def disconnect(self, fcn: Callable):
        """disconnect input by removing callback"""
        self._callbacks.remove(fcn)

    def send(self, data):
        """send data to all connected inputs"""
        for fcn in self._callbacks:
            fcn(data)


class QueueOutput:
    """output class for nodes, sends data to a queue.
    QueueOutput supports only one connected input"""

    def __init__(self) -> None:
        self._queue: Optional[asyncio.Queue] = None

    def connect(self, queue: asyncio.Queue):
        """connect receive queue"""
        assert self._queue is None, "output already connected"
        assert isinstance(queue, asyncio.Queue), "queue must be asyncio.Queue"
        self._queue = queue

    def disconnect(self):
        """disconnect queue"""
        self._queue = None

    def send(self, data):
        """send data to queue"""
        if self._queue is None:
            return  # no output connected

        self._queue.put_nowait(data)
