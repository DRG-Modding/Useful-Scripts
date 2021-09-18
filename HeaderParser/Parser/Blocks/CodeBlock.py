from __future__ import annotations
from .BlockType import BlockType
from .DumpSelfVars import DumpSelfVars
from .BlockHeader import BlockHeader
from .BlockIdentifier import BlockIdentifier
from .BlockBodyMember import BlockBodyMember
import re

# Specific block components
block_header = r"\/\/ (?P<type>[\w]+) (?P<fullName>[^ \n]+)" \
               r"(\n\/\/ Size: (?P<size>[^ ]+) \(Inherited: (?P<sizeInherited>[^)]+))?"
block_identifier = r"(?P<type>.+?) (?P<name>[^ ]+)(?: \: (?P<parent>[^ ]+))?"
block_body_member = r"(?P<type>.+?) (?P<name>[\w_\[\]]+?(?: : \d)?)(?:\((?P<params>.*)\))?;.*(?:\/\/[\W]*(?P<comment>.*))?"

re_block_header = re.compile(block_header)
re_block_identifier = re.compile(block_identifier)
re_block_body_member = re.compile(block_body_member)


class CodeBlock(DumpSelfVars):
    parent: CodeBlock = None
    children: dict[str, CodeBlock] = {}
    blockType: BlockType = None

    def __init__(self, re_block_match: re.Match, excluded: bool, source_path: str):
        self.excluded = excluded
        self.source_file = source_path

        self.header_str = re_block_match.group("header").rstrip()
        self.identifier_str = re_block_match.group("identifier").rstrip()
        self.body_str = re_block_match.group("body").rstrip()

        self.header = BlockHeader(re_block_header.search(self.header_str))
        self.identifier = BlockIdentifier(re_block_identifier.search(self.identifier_str))
        self.body_members = [BlockBodyMember(match) for match in re_block_body_member.finditer(self.body_str)]

    def class_name(self) -> str:
        return self.identifier.name[1:]
