import re
from .DumpSelfVars import DumpSelfVars
from .BrokenType import BrokenType

body_param = r"(?P<type>[^,]+) (?P<name>[^,]+?)(?:(?:, )|(?=\Z))"
re_body_param = re.compile(body_param)


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
