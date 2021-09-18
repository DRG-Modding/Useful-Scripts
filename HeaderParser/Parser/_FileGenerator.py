import os, re
from .Blocks import CodeBlock
from .CodeBlockGenerationTools import CBT
from ._Templates import _Templates


class _FileGenerator(_Templates):

    def generate_enums(self):
        with open(os.path.join(self.config.OUTPUT_DIR, "enums.h"), "w") as f:
            f.write(self.template("enums.h", {}))

            for enum in self.enums:
                if not enum.excluded:
                    f.write(CBT(self, enum).generate_enum() + "\n\n")

    @staticmethod
    def _check_body_members_subtypes(struct: CodeBlock,
                                     current_tier: dict[str, CodeBlock], next_tier: dict[str, CodeBlock]):
        for body_member in struct.body_members:
            for t in body_member.subtypes:
                if t in current_tier:
                    next_tier[struct.identifier.realname] = current_tier.pop(struct.identifier.realname)
                    return

    def generate_classes(self):
        classes = []
        includes_override = list(self._finc(["classes_fw.h"]))  # TODO: remove
        includes_override = []
        for cls in [c for c in self.classes.values() if not c.excluded]:
            path = os.path.join(self.config.OUTPUT_DIR, os.path.basename(cls.source_file))
            os.makedirs(path, exist_ok=True)
            name = cls.class_name()[1:]
            classes.append(cls.identifier.name)

            header, include_names = CBT(self, cls).generate_class_header_and_includes()
            source = CBT(self, cls).generate_class_source()

            include_names = sorted(include_names, key=lambda x: (x[0] == x[0].upper(), x))
            fw = map(lambda cls: f"class {cls.split('.')[0]};",
                     (i for i in include_names if i[0] == i[0].upper()))
            includes = self._finc(include_names)

            if includes_override is not None:
                includes = [*includes_override, *map(lambda inc: f"// {inc}", includes)]

            with open(os.path.join(path, f"{name}.h"), "w") as fh:
                fh.write(self.template("class.h", {"name": name, "includes": "\n".join(includes),
                                                   "forward_declatarions": "\n".join(fw)}))
                fh.write(header + "\n")
            with open(os.path.join(path, f"{name}.cpp"), "w") as fs:
                fs.write(self.template("class.cpp", {"name": name}))
                fs.write(source + "\n")
        with open(os.path.join(self.config.OUTPUT_DIR, "classes_fw.h"), "w") as f:
            f.write(self.template("classes_fw.h", {}))
            for cls in classes:
                f.write(f"class {cls};\n")
