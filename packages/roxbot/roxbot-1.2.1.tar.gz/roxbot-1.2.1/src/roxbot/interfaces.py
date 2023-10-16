#!/usr/bin/env python3
"""
 common interface definitions

 Copyright (c) 2023 ROX Automation
"""

from typing import NamedTuple, Tuple
from roxbot.converters import (
    latlon_to_enu,
    theta_to_heading,
    heading_to_theta,
    enu_to_latlon,
)


class Pose(NamedTuple):
    """2D pose interface"""

    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0

    @property
    def xy(self) -> Tuple[float, float]:
        return self.x, self.y

    @classmethod
    def from_gps(cls, lat: float, lon: float, heading: float) -> "Pose":
        """create pose from gps coordinates"""
        x, y = latlon_to_enu((lat, lon))
        theta = heading_to_theta(heading)

        return cls(x, y, theta)

    def to_gps(self) -> Tuple[float, float, float]:
        """convert pose to gps coordinates"""
        lat, lon = enu_to_latlon(self.xy)
        heading = theta_to_heading(self.theta)

        return lat, lon, heading

    def __str__(self) -> str:
        return f"x={self.x:.3f}, y={self.y:.3f}, theta={self.theta:.3f}"
