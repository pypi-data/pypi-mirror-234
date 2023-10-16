#!/usr/bin/env python3
"""

 Copyright (c) 2023 ROX Automations
"""
# type: ignore

import math

import numpy as np
import pytest
from pytest import approx
from roxbot import converters

from roxbot.vectors import Vector, Line, distance_to_b, distance_to_line, point_on_line


def almost_equal(v1: Vector, v2: Vector, tolerance: float = 1e-3) -> bool:
    """Checks if two Vectors are almost equal within a given tolerance."""
    return abs(v1.x - v2.x) < tolerance and abs(v1.y - v2.y) < tolerance


def test_create():
    a = Vector(0, 1)

    x, y = a
    assert x == 0
    assert y == 1

    phi = math.radians(60)
    b = Vector.from_polar(1, phi)

    assert a.x == 0
    assert a.y == 1
    assert a.xy == (0, 1)
    assert a.r == 1
    assert a.rphi == (1, math.radians(90))

    assert b.r == 1
    assert b.phi == phi
    assert b.x == math.cos(phi)
    assert b.y == math.sin(phi)
    assert abs(b) == 1

    assert repr(a) == "<Vector(x=0.000, y=1.000)>"
    _ = str(a)


def test_math():
    """basic math operations"""

    a = Vector(0, 1)
    b = Vector(1, 0)

    assert a + 1 == Vector(1, 2)
    assert a - 1 == Vector(-1, 0)

    assert a + b == Vector(1, 1)
    assert a - b == Vector(-1, 1)

    assert a + b == b + a
    assert a * b == b * a

    # components
    assert Vector(2, 0).u == Vector(1, 0)
    assert Vector(2, 0).v == Vector(0, 1)

    assert a.translate(2, 2) == a + Vector(2, 2)

    assert b.rotate(math.radians(90)) == a

    # simple multiplication
    c = Vector(2, 4)
    assert c * 2 == Vector(4, 8)
    assert 2 * c == Vector(4, 8)

    # dot product
    assert a.dot(b) == 0
    assert b.dot(a) == 0
    assert a.dot(b) == b.dot(a)

    # division
    assert c / 2.0 == Vector(1, 2)
    assert c / Vector(1, 2) == Vector(2, 2)

    # negation
    assert -a == Vector(0, -1)

    # cross
    assert np.cross(a, b) == a.cross(b)

    # angle
    assert a.angle() == math.radians(90)
    assert b.angle() == 0
    assert a.angle(b) == math.radians(90)
    assert b.angle(a) == -math.radians(90)


def test_lines():
    """line math features"""

    pa = Vector(1, 1)
    pb = Vector(3, 3)
    pc = Vector(1, 3)

    assert point_on_line(pa, pb, pc) == Vector(2, 2)

    a = Vector(0, 0)
    b = Vector(1, 0)
    c = Vector(0.5, 0.5)

    p = point_on_line(a, b, c)
    assert p == Vector(0.5, 0)

    dst = distance_to_line(a, b, c)
    assert dst == 0.5

    dst = distance_to_b(a, b, c)
    assert dst == 0.5

    c = Vector(0.8, 1)
    dst = distance_to_b(a, b, c)
    assert dst == approx(0.2)


def test_from_latlon():
    """test conversion from latlon to vector"""

    latlon = (51.365948, 6.172037)

    converters.set_gps_ref(*latlon)

    v = Vector.from_latlon(latlon)
    assert v.x == approx(0.000000)
    assert v.y == approx(0.000000)


def test_to_latlon():
    """conversion from vector to latlon"""

    latlon = (51.365948, 6.172037)
    converters.set_gps_ref(*latlon)

    v = Vector(0, 0)

    lat, lon = v.latlon
    assert lat == approx(latlon[0])
    assert lon == approx(latlon[1])


def test_line_initialization():
    l = Line(Vector(0, 0), Vector(1, 1))
    assert l.start == Vector(0, 0)
    assert l.end == Vector(1, 1)

    # repr
    _ = repr(l)


def test_line_shift_y():
    l = Line(Vector(0, 0), Vector(0, 1))
    l.shift_y(1)
    assert l.start == Vector(-1, 0)
    assert l.end == Vector(-1, 1)

    # Test for another shift
    l.shift_y(-1)
    assert l.start == Vector(0, 0)
    assert l.end == Vector(0, 1)


@pytest.mark.parametrize(
    "start, end, dy, shifted_start, shifted_end",
    [
        (Vector(0, 0), Vector(1, 1), 1, Vector(-0.707, 0.707), Vector(0.293, 1.707)),
        (Vector(1, 1), Vector(2, 2), -1, Vector(1.707, 0.293), Vector(2.707, 1.293)),
    ],
)
def test_line_shift_y_parametrized(start, end, dy, shifted_start, shifted_end):
    l = Line(start, end)
    l.shift_y(dy)
    assert almost_equal(l.start, shifted_start)
    assert almost_equal(l.end, shifted_end)
