from roxbot.topics import Topics


def test_class_attributes():
    """Test class attributes log and heartbeat."""
    assert Topics.log == "/log"
    assert Topics.heartbeat == "/heartbeat"


def test_generated():
    # instantiate a Topics object with a node name
    topics = Topics("io1")

    # test that the command and response topics are generated correctly
    assert topics.command == "/io1/cmd"
    assert topics.response == "/io1/response"
