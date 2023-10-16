#!/usr/bin/env python3
"""
Simple websocket bridge for interfacing with ui etc.

Copyright (c) 2023 ROX Automation - Jev Kuznetsov

**Protocol definition**

`(dest, data)`
* `dest` is a string, topic to post on
* `data` is a json serializable object

** how it works **

* sending: `WS_Bridge.send(dest, data)` to send data to topic on all connected clients
* receiving: add callbacks with `WS_Bridge.register_callback(dest, fcn)`. On incomng data the bridge will execute `fcn(data)`
* forwarding log messages: `WS_Brige.add_log_handler(log)` to forward log messages to `/log` topic


"""

import asyncio
import json
import logging

from typing import List, Set, Union, Dict

import websockets


from .base import Bridge

DEFAULT_PORT = 9095

Q_LENGTH = 50

log = logging.getLogger()

# set websockets logging level to info
logging.getLogger("websockets").setLevel(logging.INFO)


class WS_Bridge(Bridge):
    """websocket bridge for interfacing with ui etc."""

    def __init__(self, listen_on: str = "0.0.0.0", port: int = DEFAULT_PORT):
        super().__init__(self.__class__.__name__)

        self._host = listen_on
        self._port = port

        self._connections: Set = set()  # all current connections
        self._tasks: List = []  # keep running tasks to avoid garbage collection

        self._out_q: asyncio.Queue = asyncio.Queue(Q_LENGTH)

    async def _handle_connection(self, websocket):
        """pass this to websockets.serve"""
        self._log.debug("Established connection")

        self._connections.add(websocket)
        self._tasks.append(asyncio.create_task(self._receive_handler(websocket)))

        try:
            await websocket.wait_closed()
        finally:
            self._connections.remove(websocket)

    async def _receive_handler(self, websocket):
        """handle incoming messages"""
        async for message in websocket:
            self._log.debug("<%s", message)
            self._execute_command(message)

    async def _send_messages(self):
        """send queque items to clients"""

        while True:
            msg = await self._out_q.get()

            if self._connections:
                self._log.debug(">%s", msg)
                websockets.broadcast(self._connections, msg)  # type: ignore # pylint: disable=no-member
            else:
                self._log.debug("Dropped %s", msg)

            self._log.debug("queue length = %s", self._out_q.qsize())
            self._out_q.task_done()

    def send(self, topic: Union[str, Dict], data):
        """send data to topic"""
        self._log.debug("Sending topic=%s data=%s", topic, data)
        msg = json.dumps((topic, data))

        self._out_q.put_nowait(msg)

    async def serve(self):
        """start bridge server"""

        await websockets.serve(self._handle_connection, self._host, self._port)  # type: ignore # pylint: disable=no-member
        self._tasks.append(asyncio.create_task(self._send_messages()))
        self._tasks.append(asyncio.create_task(self._handle_logging()))

    def stop(self):
        """stop bridge server"""
        for task in self._tasks:
            task.cancel()


async def echo(host="localhost", port=DEFAULT_PORT):
    """echo all data received on port"""

    async with websockets.connect(f"ws://{host}:{port}") as websocket:  # type: ignore # pylint: disable=no-member
        async for message in websocket:
            print(message)
