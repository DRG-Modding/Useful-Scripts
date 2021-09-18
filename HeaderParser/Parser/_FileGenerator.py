import os, re
from .blocks import *
from ._Data import _Data
from ._Templates import _Templates


class _FileGenerator(_Templates):

    def generate_enums(self):
        with open(os.path.join(self.config.OUTPUT_DIR, "enums.h"), "w") as f:
            f.write(self.template("enums.h", {}))

            for enum in self.enums:
                if not enum.excluded:
                    f.write(enum.generate_enum() + "\n\n")

    @staticmethod
    def _check_body_members_subtypes(struct: CodeBlock,
                                     current_tier: dict[str, CodeBlock], next_tier: dict[str, CodeBlock]):
        for body_member in struct.body_members:
            for t in body_member.subtypes:
                if t in current_tier:
                    next_tier[struct.identifier.name] = current_tier.pop(struct.identifier.name)
                    return

    def get_sorted_structs(self) -> list[CodeBlock]:
        struct_tiers: list[dict[str, CodeBlock]] = \
            [{s.identifier.name: s for s in self.structs.values()}]
        i = 0
        while len(struct_tiers[i]) > 0:
            struct_tiers.append({})
            for struct in list(struct_tiers[i].values()):
                self._check_body_members_subtypes(struct, struct_tiers[i], struct_tiers[i + 1])
            i += 1
        return [value for tier in struct_tiers for value in tier.values()]

    def generate_structs(self):
        with open(os.path.join(self.config.OUTPUT_DIR, "structs.h"), "w") as f:
            f.write(self.template("structs.h", {}))

            for struct in self.get_sorted_structs():
                if not struct.excluded:
                    f.write(struct.generate_struct() + "\n\n")


            #for s in sorted((struct.generate_struct() for struct in self.structs.values()),
            #                key=lambda x: len(re.findall("(^|\n)[^/\n]*struct", x))):
            #    f.write(s + "\n\n")

    def generate_classes(self):
        for cls in [c for c in self.classes.values() if not c.excluded]:
            path = os.path.join(self.config.OUTPUT_DIR, os.path.basename(cls.source_file))
            os.makedirs(path, exist_ok=True)
            name = cls.class_name()
            with open(os.path.join(path, f"{name}.h"), "w") as fh:
                header, includes = cls.generate_class_and_includes(self.classes)
                fh.write(self.template("class.h", {"name": name, "includes": includes}))
                fh.write(header + "\n")
