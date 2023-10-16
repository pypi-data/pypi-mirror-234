""" test Bridge base class"""

# pylint: disable=protected-access

import json
from roxbot.bridges.base import Bridge


class DummyBridge(Bridge):
    """dummy implementation of Bridge for testing"""

    def __init__(self):
        super().__init__()

    def send(self, topic: str, data):
        pass

    async def serve(self):
        pass


def callback_no_args():
    return "success"


def callback_with_args(arg):
    return arg * 2


def test_register_callback():
    bridge = DummyBridge()

    bridge.register_callback("test_topic", callback_no_args)
    assert "test_topic" in bridge._cmd_callbacks


def test_remove_callback():
    bridge = DummyBridge()

    bridge.register_callback("test_topic", callback_no_args)
    bridge.remove_callback("test_topic")
    assert "test_topic" not in bridge._cmd_callbacks


def test_execute_command_simple():
    bridge = DummyBridge()

    bridge.register_callback("test_cmd", callback_no_args)
    ret = bridge._execute_command("test_cmd")
    assert ret == "success"


def test_execute_command_with_args():
    bridge = DummyBridge()

    bridge.register_callback("test_cmd", callback_with_args)
    ret = bridge._execute_command(json.dumps(["test_cmd", "hello"]))
    assert ret == "hellohello"
    ret = bridge._execute_command(json.dumps(["test_cmd", 2]))
    assert ret == 4

    # no args, when args are expected
    ret = bridge._execute_command("test_cmd")
    assert ret is None


def test_execute_command_not_registered():
    bridge = DummyBridge()
    ret = bridge._execute_command("not_registered_cmd")
    assert ret is None
