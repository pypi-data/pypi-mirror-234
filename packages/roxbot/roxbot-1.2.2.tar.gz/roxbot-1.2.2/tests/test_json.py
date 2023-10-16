import io
import json


import pytest

from roxbot.json import dump as orjson_dump
from roxbot.json import dumps as orjson_dumps
from roxbot.json import load as orjson_load
from roxbot.json import loads as orjson_loads

# Sample data for testing
sample_data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "is_student": False,
    "grades": [85, 90, 78],
    "address": {"street": "123 Main St", "zipcode": "12345"},
}


def test_dumps_same_as_json():
    # Compare deserialized objects since the serialized strings may differ in whitespace
    assert orjson_loads(orjson_dumps(sample_data)) == json.loads(
        json.dumps(sample_data)
    )


def test_loads_same_as_json():
    sample_json = json.dumps(
        sample_data
    )  # Use json module to generate the reference JSON string
    assert orjson_loads(sample_json) == json.loads(sample_json)


def test_dump_same_as_json():
    buffer_orjson = io.StringIO()
    buffer_json = io.StringIO()

    orjson_dump(sample_data, buffer_orjson)
    json.dump(sample_data, buffer_json)

    # Compare deserialized objects from the dumped content
    assert orjson_loads(buffer_orjson.getvalue()) == json.loads(buffer_json.getvalue())


def test_load_same_as_json():
    buffer_orjson = io.StringIO(json.dumps(sample_data))
    buffer_json = io.StringIO(json.dumps(sample_data))

    assert orjson_load(buffer_orjson) == json.load(buffer_json)
