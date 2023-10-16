"""
 utility functions and classes

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""

import math


def sign(x):
    """sign of a number"""
    if x == 0:
        return 0
    return math.copysign(1, x)
