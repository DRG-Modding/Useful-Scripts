from __future__ import annotations
import re
from .DumpSelfVars import DumpSelfVars
from .BrokenType import BrokenType
if False: from .CodeBlock import CodeBlock

body_param = r"(?P<type>[^,]+) (?P<name>[^,]+?)(?:(?:, )|(?=\Z))"
re_body_param = re.compile(body_param)


class BlockBodyMember(DumpSelfVars, BrokenType):
    function: bool = False
    params: list[dict[str, str]] = None

    def __init__(self, re_body_match: re.Match):
        if re_body_match.group("params") is not None:
            self.function = True
            self.params = list(map(lambda x: x.groupdict(),
                                   re_body_param.finditer(re_body_match.group("params"))))
        self.type = re_body_match.group("type")
        self.name = re_body_match.group("name")
        self.comment = re_body_match.group("comment")

    def is_delegate(self) -> bool:
        return not self.function and self.type == "FMulticastInlineDelegate"

    def is_member(self) -> bool:
        return not self.function and not self.is_delegate()

    def valid(self) -> str:
        return '// ' if self.invalid else ''

    def join_params(self) -> str:
        assert self.function
        return ', '.join((p['type']+' '+p['name'] for p in self.params))

    def get_return(self) -> str:
        assert self.function
        s = "return "
        if self.outer_type == "void":
            pass
        elif "*" in self.outer_type:
            s += "NULL"
        else:
            s += f"*({self.type}*)NULL"
        return s+";"

    # --- class members ---
    def generate_delegate_declaration(self) -> str:
        assert self.is_delegate()
        return f"{self.valid()}DECLARE_DYNAMIC_MULTICAST_DELEGATE(F{self.name}); // {self.comment}"

    def generate_delegate(self) -> str:
        assert self.is_delegate()
        return f"{self.valid()}UPROPERTY(BlueprintAssignable, VisibleAnywhere) " \
               f"F{self.name} {self.name}; // {self.comment}"

    def generate_class_variable(self) -> str:
        assert self.is_member()
        return f"{self.valid()}UPROPERTY(EditAnywhere, BlueprintReadWrite) " \
               f"{self.type} {self.name}; // {self.comment}"

    def generate_function_declaration(self) -> str:
        assert self.function
        return f"{self.valid()}UFUNCTION(BlueprintCallable) " \
               f"{self.type} {self.name}({self.join_params()});"

    def generate_function(self, classname: str) -> str:
        assert self.function
        return f"{self.valid()} {self.type} {classname}::{self.name}({self.join_params()}) " \
               f"{{ {self.get_return()} }}"
    # ---

    # Override to also fix function parameters
    def fix_type_name_and_set_subtypes(self, all_structs: dict[str, CodeBlock]) -> bool:
        ok = super().fix_type_name_and_set_subtypes(all_structs)
        if not self.function:
            return ok
        for param in self.params:
            param["type"] = self.type_replacements(param["type"])
            type, name = param["type"], param["name"]
            newtype, subtypes = self.get_fixed_type_name_and_subtypes(type, all_structs)
            self.subtypes |= set(t.strip("*") for t in subtypes)
            if newtype is None:
                ok = False
            else:
                param["type"] = newtype
        return ok

    def invalidate_if_param_exists_in_class_scope(self, cls: CodeBlock) -> bool:
        if not self.function:
            return False
        for param in self.params:
            for bm in cls.body_members:
                if bm.name == param["name"]:
                    self.invalid = True
                    return True
        return False
