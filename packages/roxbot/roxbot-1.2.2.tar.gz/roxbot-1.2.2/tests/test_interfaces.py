from unittest.mock import patch

from pytest import approx

from roxbot.interfaces import Pose

# pylint: disable=unused-argument


def test_pose():
    p = Pose(1, 2, 3)

    assert p.xy == (1, 2)


def test_pose_from_gps():
    p = Pose.from_gps(51, 6, 90)

    assert p.xy == (0, 0)
    assert p.theta == approx(0)


def test_default_values():
    pose = Pose()
    assert pose.x == 0.0
    assert pose.y == 0.0
    assert pose.theta == 0.0


def test_xy_property():
    pose = Pose(2.5, 3.5, 0.5)
    assert pose.xy == (2.5, 3.5)


@patch("roxbot.interfaces.heading_to_theta", return_value=0.5)
@patch("roxbot.interfaces.latlon_to_enu", return_value=(1.0, 2.0))
def test_from_gps(mocked_heading_to_theta, mocked_latlon_to_enu):
    lat, lon, heading = 10.0, 20.0, 45.0
    pose = Pose.from_gps(lat, lon, heading)
    assert pose.x == 1.0
    assert pose.y == 2.0
    assert pose.theta == 0.5


@patch("roxbot.interfaces.enu_to_latlon", return_value=(10.0, 20.0))
@patch("roxbot.interfaces.theta_to_heading", return_value=45.0)
def test_to_gps(mocked_enu_to_latlon, mocked_theta_to_heading):
    pose = Pose(2.5, 3.5, 0.5)
    assert pose.to_gps() == (10.0, 20.0, 45.0)


def test_str_representation():
    pose = Pose(2.123456, 3.123456, 0.123456)
    assert str(pose) == "x=2.123, y=3.123, theta=0.123"
