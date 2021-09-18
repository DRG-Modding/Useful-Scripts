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
block_body_member = r"(?P<type>.+?) (?P<name>[\w_\[\]]+?(?: : \d)?)(?:\((?P<params>.*)\))?;.*//[\W]*(?P<comment>.*)"

re_block_header = re.compile(block_header)
re_block_identifier = re.compile(block_identifier)
re_block_body_member = re.compile(block_body_member)


class CodeBlock(DumpSelfVars):
    parent: CodeBlock = None
    children: dict[str, CodeBlock] = {}
    blockType: BlockType = None

    def __init__(self, re_block_match: re.Match, excluded: bool, source=""):
        self.excluded = excluded
        self.source_file = source

        self.header_str = re_block_match.group("header").rstrip()
        self.identifier_str = re_block_match.group("identifier").rstrip()
        self.body_str = re_block_match.group("body").rstrip()

        self.header = BlockHeader(re_block_header.search(self.header_str))
        self.identifier = BlockIdentifier(re_block_identifier.search(self.identifier_str))
        self.body_members = [BlockBodyMember(match) for match in re_block_body_member.finditer(self.body_str)]

    def class_name(self) -> str:
        return self.identifier.name[1:]

    def fix_type_names(self, all_structs: dict[str, CodeBlock]):
        c = int(self.identifier.fix_type_name(all_structs))
        c += sum((bm.fix_type_name(all_structs) for bm in self.body_members))
        return c

    def generate_enum(self) -> str:
        return self.header_str + \
               f"\nUENUM(BlueprintType)\n" \
               f"{self.identifier_str.replace('_t', '')} {{" \
               f"{self.body_str}\n}};"

    def generate_class_and_includes(self, all_classes: dict[str, CodeBlock]) -> (str, list[str]):
        self.body_members.sort(key=lambda bm: (bm.type, bm.name))
        s = [self.header_str]
    # Delegate declaration
        delegates = [bm for bm in self.body_members if bm.is_delegate()]
        s += [bm.generate_delegate_declaration() for bm in delegates]
    # Class/struct name
        if self.blockType == BlockType.Struct:
            s.append("USTRUCT(BlueprintType)")
        s.append(f"class FSD_API {self.identifier.name} " +
                 (f": public {self.identifier.parent} " if self.identifier.parent is not None else "") + "{")
    # - Body -
        if self.blockType == BlockType.Struct:
            s.append(f"\tGENERATED_USTRUCT_BODY();")
        else:
            s.append(f"\tGENERATED_BODY()\npublic:\n// ---- Delegates ----")
        # struct should have no delegates
        assert self.blockType == BlockType.Struct and len(delegates) == 0 or self.blockType != BlockType.Struct
        s += ["\t" + bm.generate_delegate() for bm in delegates]
        s += ["", "// ---- Variables ----"]
        includes = set()
        for bm in self.body_members:
            if not bm.is_member(): continue
            if bm.Enum:     includes.add("enums.h")
            #if bm.Struct:   includes.add("structs.h")

            ue_natives = []
            for type in bm.subtypes:
                if type in all_classes:
                    if all_classes[type].excluded:
                        ue_natives.append(all_classes[type].identifier.name)
                    else:
                        includes.add(f"{all_classes[type].class_name()}.h")
                    #s += bm.subtypes
            if len(ue_natives) > 0:
                s += [f"// !!! UE native types ({', '.join(ue_natives)}) are not #included automatically !!!"]
            s += ["\t" + bm.generate_class_variable()]
        s.append("}")
        if self.parent is not None and not self.parent.excluded:
            includes.add(f"{self.parent.class_name()}.h")
        return "\n".join(s), sorted(includes, key=lambda x: (x[0] == x[0].upper(), x))