#!/usr/bin/env python3
"""
 Drop-in replacement for json module that uses orjson, which is faster than the built-in json module.

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""


import orjson

# pylint: disable=unused-argument


# json_orjson.py (updated)

import orjson


def dump(obj, fp, *args, **kwargs) -> None:
    """
    Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).
    """
    serialized = dumps(obj)
    fp.write(serialized)


def dumps(obj, *args, **kwargs) -> str:
    """
    Serialize obj to a JSON formatted string.
    """
    return orjson.dumps(obj).decode("utf-8")  # pylint: disable=no-member


def load(fp, *args, **kwargs) -> object:
    """
    Deserialize fp (a .read()-supporting file-like object) to a Python object.
    """
    content = fp.read()
    return loads(content)


def loads(s: str, *args, **kwargs) -> object:
    """
    Deserialize a JSON formatted string to a Python object.
    """

    return orjson.loads(s.encode("utf-8"))  # pylint: disable=no-member
