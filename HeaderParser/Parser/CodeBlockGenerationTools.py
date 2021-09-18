from .Blocks.CodeBlock import CodeBlock, BlockType, BlockBodyMember
from ._Data import _Data


class CBT:  # Code Block Tools
    
    def __init__(self, data:_Data, block: CodeBlock):
        self.block = block
        self.data = data
        assert len(self.data.classes) > 0
        assert len(self.data.structs) > 0
        
    def fix_type_names(self) -> (int, int):
        c = int(self.block.identifier.fix_type_name_and_set_subtypes(self.data.structs))
        c += sum((bm.fix_type_name_and_set_subtypes(self.data.structs) for bm in self.block.body_members))
        fcns = sum((bm.invalidate_if_param_exists_in_class_scope(self.block) for bm in self.block.body_members))
        return c, fcns

    def generate_enum(self) -> str:
        B = self.block
        assert B.blockType == BlockType.Enum
        return B.header_str + \
               f"\nUENUM(BlueprintType)\n" \
               f"{B.identifier_str.replace('_t', '')} {{" \
               f"{B.body_str}\n}};"

    def get_body_member_includes_and_ue_natives(self, bm: BlockBodyMember) -> (set[str], set[str]):
        """
        Determine headers that have to be included for this BlockBodyMember (class variable type)
        """
        assert bm.is_member() or bm.function
        includes, ue_natives = set(), set()

        if bm.Enum:
            includes.add("enums.h")

        ue_natives = []
        for type in bm.subtypes:
            if type in self.data.classes:
                if self.data.classes[type].excluded:
                    ue_natives.append(self.data.classes[type].identifier.name)
                else:
                    includes.add(f"{self.data.classes[type].class_name()}.h")
                # s += bm.subtypes
        return includes, ue_natives

    def _append_members(self, s: list[str], includes: set[str], functions: bool):
        for bm in [bm for bm in self.block.body_members if (bm.function if functions else bm.is_member())]:
            incs, ue_natives = self.get_body_member_includes_and_ue_natives(bm)
            for inc in incs:
                includes.add(inc)

            if len(ue_natives) > 0:
                s.append(f"// !!! UE native types ({', '.join(ue_natives)}) are not #included automatically !!!")
            s.append("\t" + (bm.generate_function_declaration() if functions else bm.generate_class_variable()))

    def generate_class_header_and_includes(self) -> (str, set[str]):
        B = self.block
        assert B.blockType in (BlockType.Struct, BlockType.Class)
        
        B.body_members.sort(key=lambda bm: (bm.type, bm.name))
        s = [B.header_str]
    # Delegate declaration
        delegates = [bm for bm in B.body_members if bm.is_delegate()]
        s += [bm.generate_delegate_declaration() for bm in delegates]
    # Class/struct name
        if B.blockType == BlockType.Struct:
            s.append("USTRUCT(BlueprintType)\nstruct ")
        elif B.blockType == BlockType.Class:
            s.append(f"UCLASS(Blueprintable, ClassGroup=(Custom))\nclass FSD_API ")
        else:
            raise Exception(f"{B.blockType} is not a struct or a class\n{B}")
        s[-1] += f"{B.identifier.name} " + \
                 (f": public {B.identifier.parent} " if B.identifier.parent is not None else "") + "{"
    # - Body -
        if B.blockType == BlockType.Struct:
            s.append(f"\tGENERATED_USTRUCT_BODY();\n")
        else:
            s.append(f"\tGENERATED_BODY()\n\npublic:\n// ---- Delegates ----")
        # struct should have no delegates
        assert B.blockType == BlockType.Struct and len(delegates) == 0 or B.blockType != BlockType.Struct
        s += ["\t" + bm.generate_delegate() for bm in delegates]

        s += ["", "// ---- Variables ----"]
        includes = set()
        self._append_members(s, includes, False)

        s += ["", "// ---- Functions ----"]
        self._append_members(s, includes, True)

        s.append("};")
        if B.parent is not None and not B.parent.excluded:  # Include parent class
            includes.add(f"{B.parent.class_name()}.h")
        return "\n".join(s), includes

    def generate_class_source(self) -> str:
        s = []
        for bm in [bm for bm in self.block.body_members if bm.function]:
            s.append(f"{bm.generate_function(self.block.identifier.name)}")
        return "\n".join(s)



