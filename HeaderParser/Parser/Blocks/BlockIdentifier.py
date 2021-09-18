import re
from .DumpSelfVars import DumpSelfVars
from .BrokenType import BrokenType


class BlockIdentifier(DumpSelfVars, BrokenType):

    def __init__(self, re_identifier_match: re.Match, virtual_name=None):
        if virtual_name is None:  # deprecated
            self.type = re_identifier_match.group("type")
            self.name = re_identifier_match.group("name")
            self.parent = re_identifier_match.group("parent")
        else:
            self.type = ""
            self.parent = None
            self.name = virtual_name
