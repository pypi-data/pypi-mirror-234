#!/usr/bin/env python3
"""
 ws_bridge client for testing interface.

 This is a bit unconventional testing, as it tests integral interaction between
    the server and client.

 enable logging to see debug messages
 `pytest --log-cli-level=debug`

 Copyright (c) 2022 ROX Automation - Jev Kuznetsov
"""


import asyncio
import json
import logging
import websockets

from roxbot.bridges.ws_bridge import WS_Bridge

PORT = 9999

# create and start server
bridge = WS_Bridge(port=PORT)
result = -1


# logging
log = logging.getLogger("bridge_test")


async def client():
    async with websockets.connect("ws://localhost:%i" % PORT) as websocket:  # type: ignore # pylint: disable=no-member
        # some invalid requests

        # loopback test bridge -> client
        idx = 42
        bridge.send("loopback", idx)  # send data through bridge to itself.

        resp = await websocket.recv()
        topic, data = json.loads(resp)
        assert topic == "loopback"
        assert data == idx

        for idx in range(11):
            # send command to server
            await websocket.send(json.dumps(["/tst", idx]))
            # wait a bit
            await asyncio.sleep(0.01)
            # global result is set by callback
            assert result == idx


def example_cbk(data):
    global result  # pylint: disable=global-statement
    logging.info("callback called with %s", data)
    result = data


async def run_test():
    bridge.register_callback("/tst", example_cbk)

    await bridge.serve()

    await asyncio.wait_for(client(), timeout=1.0)


# ---------------- test functions


def test_server():
    asyncio.run(run_test())
    assert result == 10
