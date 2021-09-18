from .Blocks import CodeBlock, BlockType, VirtualBlock
from ._Data import _Data
import os, re

# Initial general block regex
re_block = re.compile(
    r"(?P<header>(?:\/\/.*\n)+)+"
    r"(?P<identifier>[^\{\/]+)"
    r" {(?P<body>(?:\n|.)+?)};\n"
)
excluded_classes = {"_C", }


class _DataLoader(_Data):

    def __init__(self, *args):
        self.init(*args)
        print("Loading blocks from header files... ", end="")
        self._load_blocks(self.config.WORKING_DIR, False)
        self._load_blocks(self.config.CONFLICT_DIR, True)
        print(len(self._blocks), "loaded.")

        print("Enums: ", end="")
        self._find_enums()
        print(len(self.enums))

        print("Matching parents... ", end="")
        d, t = self._find_parents()
        print(f"{t} blocks matched to {d} distinct parent block.")

        print("Creating virtual parents... ", end="")
        # deprecated, UE headers are now loaded and marked as excluded=True
        n, t = self._create_virtual_parents()
        assert n == 0  # if not all blocks are present, then struct/class inheritance will break
        print(f"{n} virtual parent blocks created for {t} child blocks.")

        s, p = self._find_top_level_parent_blocks_and_structs()
        print(f"{p} top-level parent blocks, {s} structs.")

        self._find_classes()
        print(f"{len(self.classes)} classes.")

        print("Merging structs into classes... ", end="")
        for k,v in self.structs.items():
            self.classes[k] = v
        self.structs = {}
        print(f"{len(self.classes)} classes, {len(self.structs)} structs")
        assert len(self.structs) == 0

        print("Fixing type names... ", end="")
        c = sum((block.fix_type_names(self.structs) for block in self.structs.values()))
        c += sum((block.fix_type_names(self.structs) for block in self.classes.values()))
        print(f"{c} changes made.")

    def _load_blocks(self, from_path: str, excluded: bool):
        for filename in os.listdir(from_path):
            filepath = os.path.join(from_path, filename)
            for match in re_block.finditer(open(filepath, encoding="UTF-8").read()):
                self._blocks.append(CodeBlock(match, excluded, filepath))
        return len(self._blocks)

    def _find_parents(self):
        """ Match parent classes to blocks """
        different = 0
        existing = 0
        for block in self._blocks:
            if block.identifier.parent is None:
                continue
            if block.identifier.parent in self.parent_blocks:
                block.parent = self.parent_blocks[block.identifier.parent]
                block.parent.children[block.identifier.name] = block
                existing += 1
                continue
            for potential_parent_block in self._blocks:
                if potential_parent_block.identifier.name == block.identifier.parent:
                    block.parent = potential_parent_block
                    block.parent.children[block.identifier.name] = block
                    self.parent_blocks[block.parent.identifier.name] = block.parent
                    different += 1
                    break
        return different, different + existing

    # Deprecated TODO: remove
    def _create_virtual_parents(self):
        """ Create "virtual" parent blocks for parent classes not found in header files """
        new = 0
        existing = 0
        for block in self._blocks:
            if block.parent is not None or block.identifier.parent is None:
                continue
            if block.identifier.parent in self.parent_blocks:
                block.parent = self.parent_blocks[block.identifier.parent]
                block.parent.children[block.identifier.name] = block
                existing += 1
                continue
            block.parent = VirtualBlock(block.identifier.parent)
            block.parent.children[block.identifier.name] = block
            self.parent_blocks[block.parent.identifier.name] = block.parent
            new += 1
        return new, new + existing

    def _find_top_level_parent_blocks_and_structs(self):
        for block in self.parent_blocks.values():
            if block.parent is None:
                self.top_level_blocks.append(block)

        return (self._find_structs(), len(self.top_level_blocks))

    def _find_structs(self):
        i = 0
        c = 0
        while i < len(self._blocks):
            block: CodeBlock = self._blocks[i]
            if block.header.type == "ScriptStruct":
                c += 1
                self.structs[block.identifier.name] = block
                block.blockType = BlockType.Struct
                self._blocks.pop(i)
                if block.identifier.name in self.top_level_blocks:
                    self.top_level_blocks.remove(block.identifier.name)
            else:
                i += 1
        return c

    def _find_enums(self):
        i = 0
        c = 0
        while i < len(self._blocks):
            block = self._blocks[i]
            if block.header.type == "Enum":
                c += 1
                block.blockType = BlockType.Enum
                self.enums.append(block)
                self._blocks.pop(i)
            else:
                i += 1
        return c

    @staticmethod
    def _is_valid_class(class_block: CodeBlock) -> bool:
        for exclusion in excluded_classes:
            if exclusion in class_block.identifier.name:
                return False
        # TEMPORARY
        #if class_block.excluded or "FSDEngine_classes" in class_block.source_file:
        #    return False
        return True

    def _find_classes(self):
        for block in self._blocks:
            block.blockType = BlockType.Class
            if self._is_valid_class(block):
                self.classes[block.identifier.name] = block

