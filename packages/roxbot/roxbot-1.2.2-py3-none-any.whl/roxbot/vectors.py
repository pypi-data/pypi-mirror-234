#!/usr/bin/env python3
"""


 Copyright (c) 2023 ROX Automation

code inspired by:

*  https://scipython.com/book2/chapter-4-the-core-python-language-ii/examples/a-2d-vector-class/ # noqa
*  https://gist.github.com/tfeldmann/4c4b56807f4447266bc6f722bf63705b
*  [vector.py](https://gist.github.com/mostley/3819375)
*  [StackOverflow](https://stackoverflow.com/a/43542669)
*  [vector.py](https://github.com/betados/vector_2d/blob/develop/vector_2d/vector.py)
*  [vectors.py](https://github.com/sjev/PythonRobotics/blob/master/PythonRobotics/vectors.py)

"""

from __future__ import annotations

import cmath
from math import atan2, cos, hypot, sin
from typing import Optional

import numpy as np
from numpy.typing import NDArray  # pylint: disable=import-error, no-name-in-module
from roxbot.converters import enu_to_latlon, latlon_to_enu


class Vector:
    """simple 2d vector class"""

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_polar(cls, r: float, phi: float) -> Vector:
        return cls(r * cos(phi), r * sin(phi))

    @property
    def xy(self) -> tuple[float, float]:
        return (self.x, self.y)

    def cross(self, other: Vector) -> float:
        """cross product"""
        return (self.x * other.y) - (self.y * other.x)

    def dot(self, other: Vector) -> float:
        """dot product"""
        return self.x * other.x + self.y * other.y

    @property
    def phi(self) -> float:
        c = complex(self.x, self.y)
        return cmath.phase(c)

    @property
    def r(self) -> float:
        """length"""
        return hypot(self.x, self.y)

    @property
    def rphi(self) -> tuple[float, float]:
        return (self.r, self.phi)

    @property
    def u(self) -> Vector:
        """normalized vector"""
        return self / abs(self)

    @property
    def v(self) -> Vector:
        """normalized perpendicular component"""
        u = self.u
        return Vector(-u.y, u.x)

    def angle(self, other: Optional[Vector] = None) -> float:
        """angle between vector, *relative* to other, range (-pi..pi)"""

        if other is None:
            other = Vector(1, 0)

        return -atan2(self.cross(other), self.dot(other))

    def translate(self, dx: float, dy: float) -> Vector:
        return self + Vector(dx, dy)

    def rotate(self, alpha: float) -> Vector:
        """rotate counter-clockwise"""

        return Vector(
            self.x * cos(alpha) - self.y * sin(alpha),
            self.x * sin(alpha) + self.y * cos(alpha),
        )

    def __abs__(self) -> float:
        return hypot(self.x, self.y)

    def __add__(self, other: Vector | float) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        return Vector(self.x + other, self.y + other)

    def __neg__(self) -> Vector:
        return self * (-1)

    def __sub__(self, other: Vector | float) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        return Vector(self.x - other, self.y - other)

    def __mul__(self, other: Vector | float) -> Vector:
        """scalar product"""
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

        return Vector(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __truediv__(self, other: Vector | float) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

        return Vector(self.x / other, self.y / other)

    def __repr__(self) -> str:
        return f"<Vector(x={self.x:.3f}, y={self.y:.3f})>"

    def __str__(self) -> str:
        return f"({self.x:.3f},{self.y:.3f})"

    def __eq__(self, other: Vector) -> bool:  # type: ignore
        return abs(self - other) < 1e-16

    def __array__(self) -> NDArray[np.float32]:
        """numpy array compatibility"""
        return np.array([self.x, self.y])

    def __getitem__(self, item):
        """make subscriptable"""
        return [self.x, self.y][item]

    @property
    def latlon(self) -> tuple[float, float]:
        """convert from xy to latlon"""
        return enu_to_latlon(self.xy)

    @classmethod
    def from_latlon(cls, latlon: tuple[float, float]) -> Vector:
        """convert from latlon to xy"""

        x, y = latlon_to_enu(latlon)
        return cls(x, y)


class Line:
    """A segment is a line between two points."""

    def __init__(self, start: Vector, end: Vector):
        self.start = start
        self.end = end

    def shift_y(self, dy: float):
        """Shifts the segment to the left by dy units.

        Args:
        - dy: Shift to the left of the line.
        """

        # Calculate the direction of the segment
        direction = (self.end - self.start).u

        # Calculate the normal to the direction (to the left)
        normal = Vector(-direction.y, direction.x)

        # Calculate the shift to the left
        shift_left = normal * dy

        # Shift the start and end points
        self.start = self.start + shift_left
        self.end = self.end + shift_left

    def __repr__(self) -> str:
        return f"<Line(start={self.start}, end={self.end})>"


def point_on_line(a: Vector, b: Vector, x: Vector) -> Vector:
    """
    project point x onto line defined by points a an b
    """
    ax = x - a
    ab = b - a
    return a + ax.dot(ab) / ab.dot(ab) * ab


def distance_to_line(a: Vector, b: Vector, x: Vector) -> float:
    """distance between point x and through points a and b"""

    p = point_on_line(a, b, x)
    return abs(x - p)


def distance_to_b(a: Vector, b: Vector, x: Vector) -> float:
    """distance to endpoint along line. negative if behind b"""
    ab = b - a
    px = b - x
    dst = ab.dot(px) / abs(ab)

    return dst
