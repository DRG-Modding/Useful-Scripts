import re

inner_type = r"(.*?)<(.*)>"
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