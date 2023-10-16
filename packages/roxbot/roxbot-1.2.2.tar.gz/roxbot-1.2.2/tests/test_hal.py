""" tests for HAL"""

from roxbot.hal.base import DeviceType
from roxbot.hal.canopen import RemoteIO_Mock
from roxbot.bridges.mock_bridge import MockBridge


def test_device():
    """test base class"""

    dev = RemoteIO_Mock(name="test")
    assert dev.name == "test"
    assert dev.device_type == DeviceType.REMOTE_IO
    assert isinstance(dev.bridge, MockBridge)
    assert not dev.get_errors()
    assert dev.clear_errors() is None
