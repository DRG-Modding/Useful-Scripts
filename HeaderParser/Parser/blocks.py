from __future__ import annotations
import re
from .utils import DumpSelfVars
from enum import Enum, auto

# Specific block components
block_header = r"\/\/ (?P<type>[\w]+) (?P<fullName>[^ \n]+)" \
               r"(\n\/\/ Size: (?P<size>[^ ]+) \(Inherited: (?P<sizeInherited>[^)]+))?"
block_identifier = r"(?P<type>.+?) (?P<name>[^ ]+)(?: \: (?P<parent>[^ ]+))?"
#block_body_member = r"(?P<type>.+) (?P<name>[\w_]+?)(?:\((?P<params>.*)\))?;.*//[\W]*(?P<comment>.*)"
block_body_member = r"(?P<type>.+?) (?P<name>[\w_\[\]]+?(?: : \d)?)(?:\((?P<params>.*)\))?;.*//[\W]*(?P<comment>.*)"
body_param = r"(?P<type>[^,]+) (?P<name>[^,]+?)(?:(?:, )|(?=\Z))"
inner_type = r"(.*?)<(.*)>"
re_block_header = re.compile(block_header)
re_block_identifier = re.compile(block_identifier)
re_block_body_member = re.compile(block_body_member)
re_body_param = re.compile(body_param)
re_inner_type = re.compile(inner_type)


class BrokenType:
    name: str = None
    type: str = None
    invalid: bool = False
    Struct = False
    Enum = False
    Class = False

    def fix_type_name(self, all_structs : dict):
        old_type = self.type.replace("_t", "").replace("char", "uint8").strip()
        self.type, self.subtypes = self.get_fixed_type_name_and_subtypes(old_type, all_structs)
        self.subtypes = [t.strip("*") for t in self.subtypes]
        if self.type is None or "[" in self.name or "Unknown" in self.name:
            self.invalid = True
            self.type = old_type
        return old_type == self.type

    def get_fixed_type_name_and_subtypes(self, typename, all_structs: dict) -> (str, list[str]):
        inner_match = re_inner_type.search(typename)
        if inner_match is not None:
            replace_with, subtypes = self.get_fixed_type_name_and_subtypes(inner_match.group(2), all_structs)
            replace_outer_with = self._get_fixed_single_type_name(inner_match.group(1), all_structs)
            if replace_with is None or replace_outer_with is None:
                return None, []
            return typename.replace(inner_match.group(2), replace_with).replace(inner_match.group(1), replace_outer_with), \
                   subtypes + [replace_outer_with]

        new_types = [self._get_fixed_single_type_name(t.strip(), all_structs) for t in typename.split(",")]
        if None in new_types:
            return None, []
        else:
            return ", ".join(new_types), new_types

    def _get_fixed_enum_type_name(self, typename: str) -> str:
        if typename in {"ECollisionEnabled"}:
            return f"TEnumAsByte<{typename}::Type>"
        return typename

    def _get_fixed_single_type_name(self, typename: str, all_structs: dict) -> str or None:
        if BrokenType._check_invalid_typenames(typename):
            return None

        T = typename.split(" ")
        if len(T) == 3 and T[0] == "enum" and T[1] == "class":  # enum
            self.Enum = True
            return self._get_fixed_enum_type_name(T[2])
        elif len(T) > 2 and T[0]:  # invalid variable with spaces
            #print("UNKNOWN TYPE:", T)
            return None
        elif T[0] == "struct":
            if len(T) == 1:  # class
                self.Class = True
                return "class"
            elif T[1] not in all_structs:  # ?
                print(T)
                assert False
                return T[1]
        self.Struct = True
        return typename  # struct

    @staticmethod
    def _check_invalid_typenames(typename) -> bool:
        # TODO: validate exclusions
        for T in {"uint32", "int16", "None", "SoftClassProperty"}:
            if T in typename:
                return True
        #name = typename.strip().split(" ")[-1]
        #if name[0] in ["U", "A", "F", "I"]:
        #    return True
        return False


class BlockBodyMember(DumpSelfVars, BrokenType):
    def __init__(self, re_body_match: re.Match):
        if re_body_match.group("params") is not None:
            self.function = True
            self.params = list(map(lambda x: x.groupdict(),
                                   re_body_param.finditer(re_body_match.group("params"))))
        else:
            self.function = False
            self.params = None
        self.type = re_body_match.group("type")
        self.name = re_body_match.group("name")
        self.comment = re_body_match.group("comment")

    def is_delegate(self) -> bool:
        return not self.function and self.type == "FMulticastInlineDelegate"

    def is_member(self) -> bool:
        return not self.function and not self.is_delegate()

    def valid(self) -> str:
        return '// ' if self.invalid else ''

    def generate_struct_member(self) -> str:
        assert self.is_member()
        return f"{self.valid()}UPROPERTY(EditAnywhere, BlueprintReadWrite) " \
               f"{self.type} {self.name}; // {self.comment}"

    # --- class members ---
    def generate_delegate_declaration(self) -> str:
        assert self.is_delegate()
        return f"{self.valid()}DECLARE_DYNAMIC_MULTICAST_DELEGATE(F{self.name}); // {self.comment}"

    def generate_delegate(self) -> str:
        assert self.is_delegate()
        return f"{self.valid()}UPROPERTY(BlueprintAssignable, VisibleAnywhere) " \
               f"F{self.name} {self.name}; // {self.comment}"

    def generate_class_variable(self) -> str:
        return self.generate_struct_member()

    def generate_function(self) -> str:
        assert self.function
        raise NotImplementedError()
    # ---


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


class BlockIdentifier(DumpSelfVars, BrokenType):

    def __init__(self, re_identifier_match: re.Match, virtual_name=None):
        if virtual_name is None:
            self.type = re_identifier_match.group("type")
            self.name = re_identifier_match.group("name")
            self.parent = re_identifier_match.group("parent")
        else:
            self.type = ""
            self.parent = None
            self.name = virtual_name


class BlockType(Enum):
    Enum = auto()
    Struct = auto()
    Class = auto()


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

    def generate_struct_and_includes(self, all_classes: dict[str, CodeBlock]) -> (str, list[str]):
        members = []
        includes = set()
        for bm in self.body_members:

            # TODO: refactor
            ue_natives = []
            for type in bm.subtypes:
                if type in all_classes:
                    if all_classes[type].excluded:
                        ue_natives.append(all_classes[type].identifier.name)
                    else:
                        includes.add(f"{all_classes[type].class_name()}.h")
            members.append("\t" + bm.generate_struct_member())

        return self.header_str + \
               f"\nUSTRUCT(BlueprintType)\n" \
               f"struct {self.identifier.name} " + \
               (f": public {self.identifier.parent} " if self.identifier.parent is not None else "") + \
               f"{{\n" \
               f"\tGENERATED_USTRUCT_BODY();\n" + \
               '\n'.join(["\t" + bm.generate_struct_member() for bm in self.body_members]) + \
               "\n};", \
               sorted(includes, key=lambda s: (s[0] == s[0].upper(), s))

    def generate_class_and_includes(self, all_classes: dict[str, CodeBlock]) -> (str, list[str]):
        self.body_members.sort(key=lambda bm: (bm.type, bm.name))
        s = [self.header_str]
        # Delegate declaration
        delegates = [bm for bm in self.body_members if bm.is_delegate()]
        s += [bm.generate_delegate_declaration() for bm in delegates]
        # Class/struct name
        if self.blockType == BlockType.Struct:
            s += "USTRUCT(BlueprintType)"
        s.append(f"class FSD_API {self.identifier.name} " +
                 (f": public {self.identifier.parent} " if self.identifier.parent is not None else "") + "{{")
        if self.blockType == BlockType.Struct:
            s.append(f"\tGENERATED_USTRUCT_BODY();")
        else:
            s.append(f"\tGENERATED_BODY()\npublic:\n// ---- Delegates ----")
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


        if self.parent is not None and not self.parent.excluded:
            includes.add(f"{self.parent.class_name()}.h")
        return "\n".join(s), sorted(includes, key=lambda s: (s[0] == s[0].upper(), s))


class VirtualBlock:
    parent = None
    excluded = True
    children = {}

    def __init__(self, name):
        self.identifier = BlockIdentifier(None, name)

    def __repr__(self):
        return self.identifier.name
