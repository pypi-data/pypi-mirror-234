import asyncio

import pytest

from roxbot.nodes.base import CallbackOutput, Node, QueueOutput

# pylint: disable=protected-access


class DummyNode(Node):
    async def main(self):
        pass


def test_node_creation():
    node = DummyNode("TestNode")
    assert node.name == "TestNode"
    assert not node.inputs
    assert not node.outputs

    # repr
    assert repr(node) == "<DummyNode TestNode>"


def test_callback_output():
    output = CallbackOutput()
    test_data = "test_data"

    received_data = []

    def dummy_callback(data):
        received_data.append(data)

    output.connect(dummy_callback)
    output.send(test_data)

    assert test_data in received_data

    output.disconnect(dummy_callback)
    received_data.clear()
    output.send(test_data)

    assert not received_data


def test_queue_output():
    output = QueueOutput()
    test_data = "test_data"

    queue = asyncio.Queue()
    output.connect(queue)
    output.send(test_data)

    assert queue.qsize() == 1
    assert queue.get_nowait() == test_data

    output.disconnect()
    with pytest.raises(asyncio.QueueEmpty):
        queue.get_nowait()

    # now disconnected
    assert output._queue is None
    output.send(test_data)
