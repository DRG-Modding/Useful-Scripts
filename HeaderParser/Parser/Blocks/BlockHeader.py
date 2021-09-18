import re
from .DumpSelfVars import DumpSelfVars


class BlockHeader(DumpSelfVars):

    def __init__(self, re_header_match: re.Match):
        self.type = re_header_match.group("type")
        self.fullName = re_header_match.group("fullName")
        try:
            self.sizeTotal = int(re_header_match.group("size"), 16)
            self.sizeInherited = int(re_header_match.group("sizeInherited"), 16)
            self.size = self.sizeTotal - self.sizeInherited
        except:
            self.sizeTotal = 0
            self.sizeInherited = 0
            self.size = 0
