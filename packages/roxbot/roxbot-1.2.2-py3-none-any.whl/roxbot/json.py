#!/usr/bin/env python3
"""
 Drop-in replacement for json module that uses orjson, which is faster than the built-in json module.

 Copyright (c) 2023 ROX Automation - Jev Kuznetsov
"""


import orjson


from typing import Union, Dict, List, Any

JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

# pylint: disable=unused-argument


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


def load(fp, *args, **kwargs) -> JSONType:
    """
    Deserialize fp (a .read()-supporting file-like object) to a Python object.
    """
    content = fp.read()
    return loads(content)


def loads(s: str, *args, **kwargs) -> JSONType:
    """
    Deserialize a JSON formatted string to a Python object.
    """

    return orjson.loads(s.encode("utf-8"))  # pylint: disable=no-member
