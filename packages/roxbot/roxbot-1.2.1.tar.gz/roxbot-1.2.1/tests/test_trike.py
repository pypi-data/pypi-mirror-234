""" test trike model

for interactive geometry see: https://www.geogebra.org/calculator/rea6w9a2

"""
from math import radians

from pytest import approx

from roxbot.models import TrikeModel

DT = 0.1


def create_trike():
    return TrikeModel(-1.0, 1.0, wheel_accel=1e6, steer_speed=1e6)


def test_curvature_calc():
    m = create_trike()

    # straight line
    m.target_steer = 0.0
    m.step(DT)
    assert m.steering_angle == 0.0
    assert m.curvature == 0.0

    # 45 deg turn
    m.target_steer = radians(45)
    m.step(DT)
    assert m.curvature == approx(-1)

    # -45 deg turn
    m.target_steer = radians(-45)
    m.step(DT)
    assert m.curvature == approx(1)


def test_velocity_calc():
    m = create_trike()

    # straight line
    m.target_steer = 0.0
    m.target_velocity = 1.0
    m.step(DT)
    assert m.velocity == 1.0

    vels = m.wheel_targets
    assert vels[0] == approx(1.0)
    assert vels[1] == approx(1.0)

    # 45 deg turn
    m.target_steer = radians(45)
    m.step(DT)
    vl, vr = m.wheel_targets
    assert vl == approx(1.5)
    assert vr == approx(0.5)

    # other angle
    m.target_steer = radians(30.07)
    m.step(DT)
    vl, vr = m.wheel_targets
    assert vl == approx(1.289, abs=0.01)
    assert vr == approx(0.711, abs=0.01)

    # other angle
    m.target_steer = radians(-20.025)
    m.step(DT)
    vl, vr = m.wheel_targets
    assert vl == approx(0.818, abs=0.01)
    assert vr == approx(1.182, abs=0.01)

    # slow down
    m.target_velocity = 0.5
    m.target_steer = radians(-45)
    m.step(DT)
    assert m.curvature == approx(1, abs=0.001)
    vl, vr = m.wheel_targets
    assert vl == approx(0.25)
    assert vr == approx(0.75)


def test_steering_angle():
    m = create_trike()

    m.target_velocity = 1.0
    m.target_steer = 0.5
    m.step(DT)
    assert m.steering_angle == 0.5


def test_properties():
    """just call properties to make sure they don't crash"""
    m = create_trike()
    m.target_steer = 0.5
    assert m.target_steer == 0.5
    assert m.wheel_targets == (0, 0)
    assert m.curvature == 0
    _ = m.pose
