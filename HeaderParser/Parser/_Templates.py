import os
from ._Data import _Data
import datetime
from typing import Generator


class _Templates(_Data):

    def get_meta_info(self):
        dt = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        headers = self.config.ORIGINALS_DIR.strip("./")+"/"
        reloaded = f"{'' if self.config.RELOAD else 'NOT '}reloaded"
        return f"From: {headers} ({reloaded}) @ {dt}"

    @staticmethod
    def _finc(includes: list[str]) -> Generator[str, None, None]:
        return (f'#include "{s[1:] if s[0] == s[0].upper() else s}"' for s in includes)

    def template(self, name: str, format: dict):
        #format["includes"] = "\n".join(map(lambda x: f'#include "{x}"', format.get("includes", [])))
        format["includes"] = format.get("includes", "")
        template = open(os.path.join(self.config.TEMPLATE_DIR, "prefix.txt")).read()
        template += open(os.path.join(self.config.TEMPLATE_DIR, name)).read()
        return template.format(**format, meta_info=self.get_meta_info())
