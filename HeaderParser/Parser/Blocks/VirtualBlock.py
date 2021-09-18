from .BlockIdentifier import BlockIdentifier


# Deprecated TODO: remove
class VirtualBlock:
    parent = None
    excluded = True
    children = {}

    def __init__(self, name):
        self.identifier = BlockIdentifier(None, name)

    def __repr__(self):
        return self.identifier.name
