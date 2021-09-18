import os, re
from .Blocks import CodeBlock
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

    def generate_classes(self):
        for cls in [c for c in self.classes.values() if not c.excluded]:
            path = os.path.join(self.config.OUTPUT_DIR, os.path.basename(cls.source_file))
            os.makedirs(path, exist_ok=True)
            name = cls.class_name()
            with open(os.path.join(path, f"{name}.h"), "w") as fh:
                header, includes = cls.generate_class_and_includes(self.classes)
                fh.write(self.template("class.h", {"name": name, "includes": includes}))
                fh.write(header + "\n")
