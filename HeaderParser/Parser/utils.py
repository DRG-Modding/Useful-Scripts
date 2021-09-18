class DumpSelfVars:
    _pad = "  "

    def __repr__(self):
        repr_str = ""
        for k, v in vars(self).items():
            k_s = f"{self._pad}{str(k)}: "
            padding = len(k_s) + 1
            repr_str += k_s + ("'" if type(v) is str else "")
            repr_str += ("\n" + (" " * padding)).join(str(v).split("\n"))
            repr_str += ("'" if type(v) is str else "") + "\n"
        return f"{{\n{repr_str}}}"
        #return "{\n\t" + "\n\t".join([f"'{str(k)}': '{str(v)}'" for k, v in vars(self).items()]) + "\n}"