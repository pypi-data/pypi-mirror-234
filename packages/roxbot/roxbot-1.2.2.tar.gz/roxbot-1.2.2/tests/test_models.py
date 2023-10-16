import pytest
import math
from roxbot.models import LinearModel, Wheel


def test_linear_model_init():
    model = LinearModel(roc=1.0, val=5.0)
    assert model.val == 5.0
    assert model.roc == 1.0
    assert model.setpoint == 5.0

    # with setpoint
    model = LinearModel(roc=1.0, val=5.0, setpoint=10.0)
    assert model.val == 5.0
    assert model.roc == 1.0
    assert model.setpoint == 10.0

    # repr method
    assert repr(model) == "LinearModel(val=5.0, setpoint=10.0, roc=1.0)"


def test_linear_model_set_target():
    model = LinearModel(roc=1.0, val=5.0)
    model.setpoint = 10.0
    assert model.setpoint == 10.0


def test_linear_model_inf():
    """test infinite roc"""
    model = LinearModel(roc=math.inf, val=5.0)
    model.setpoint = 10.0
    model.step(1.0)
    assert model.val == 10.0


def test_linear_model_step():
    model = LinearModel(roc=1.0, val=5.0)
    model.setpoint = 10.0

    # simulate some steps
    model.step(1.0)
    assert model.val == 6.0

    model.step(1.0)
    assert model.val == 7.0

    model.step(0.5)
    assert model.val == 7.5

    # go back
    model.setpoint = 0.0
    model.step(2.5)

    assert model.val == 5.0

    model.step(5)
    assert model.val == 0.0

    model.step(5)
    assert model.val == 0.0

    # big step
    model = LinearModel(roc=10.0)
    model.setpoint = 2.0
    model.step(1)
    assert model.val == 2.0

    # negative step
    with pytest.raises(ValueError):
        model.step(-0.01)


def test_clipping():
    model = LinearModel(roc=1.0, val=5.0, min_val=-10.0, max_val=10.0)
    model.setpoint = 20.0
    model.step(1.0)
    assert model.val == 6.0

    model.step(10.0)
    assert model.val == 10.0

    model.setpoint = -20.0

    model.step(10.0)
    assert model.val == 0.0

    model.step(10.0)
    assert model.val == -10.0

    model.step(10.0)
    assert model.val == -10.0


def test_wheel():
    # create a wheel with a diameter of 1 meter and an acceleration of 1 radian per second squared # noqa
    wheel = Wheel(diameter=1.0, accel=1.0)

    # set the velocity of the wheel to 1 meter per second
    wheel.set_velocity_ms(1.0)

    # check acceleration
    wheel.step(0.5)
    assert wheel.velocity_ms == 0.5

    # simulate time passing with a time step of 10 second
    wheel.step(dt=10.0)

    # get distance
    _ = wheel.distance

    # check that the wheel's angular velocity is correct
    assert wheel.velocity_ms == 1.0

    # test repr
    assert repr(wheel) == "Wheel(rps=0.32, velocity=1.00 m/s)"


def test_wheel_max_vel():
    """test wheel with max velocity"""

    wheel = Wheel(diameter=1.0, accel=1.0, max_velocity=1.5)

    wheel.set_velocity_ms(2.0)
    wheel.step(1.0)
    assert wheel.velocity_ms == 1.0
    wheel.step(1.0)
    assert wheel.velocity_ms == 1.5

    # reverse
    wheel.set_velocity_ms(-2.0)
    wheel.step(1.0)
    assert wheel.velocity_ms == 0.5
    wheel.step(2.0)
    assert wheel.velocity_ms == -1.5


def test_wheel_properties():
    wheel = Wheel(diameter=1.0, accel=1.0)
    assert wheel.rps == 0.0
    assert wheel.revolutions == 0.0
    assert wheel.ds == 0.0
