# topic definitions


class Topics:
    """Topic definitions, instantiate with a node name to create topic names that
    include the node name. e.g. Topics("io1").command will return "/io1/cmd" """

    log = "/log"
    heartbeat = "/heartbeat"

    def __init__(self, name):
        self.name = name

    @property
    def command(self):
        return f"/{self.name}/cmd"

    @property
    def response(self):
        return f"/{self.name}/response"
