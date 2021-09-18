from .blocks import CodeBlock
import os


class _Data:
    _blocks: list[CodeBlock] = []
    parent_blocks: dict[str, CodeBlock] = {}  # key: parent block name, value: parent CodeBlock
    top_level_blocks: list[CodeBlock] = []
    structs: dict[str, CodeBlock] = {}  # key: struct name, value: struct CodeBlock
    enums: list[CodeBlock] = []
    classes: dict[str, CodeBlock] = {}  # key: class name, value: class CodeBlock

    config = None

    def init(self, config):
        self.config = config

        if not os.path.exists(self.config.WORKING_DIR):
            print("WARNING: WORKING_DIR missing, but config.RELOAD == False. \n"
                  "Cannot continue without reloading: ignoring config value and reloading anyway.")
            config.RELOAD = True

        if config.RELOAD:
            config.reload()
