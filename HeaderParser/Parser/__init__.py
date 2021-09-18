#from .blocks import *  # TODO: refactor each class into separate file
from ._DataLoader import _DataLoader
from ._FileGenerator import _FileGenerator
from .Blocks import DumpSelfVars


class Parser(DumpSelfVars, _DataLoader, _FileGenerator):

    def __init__(self, *args):
        _DataLoader.__init__(self, *args)

    def generate_files(self):
        import shutil, os

        print("Creating new output dir.")
        shutil.rmtree(self.config.OUTPUT_DIR, True)
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

        print("Generating enums...")
        self.generate_enums()
        print("OK\nGenerating classes and structs...")
        self.generate_classes()
        print("OK")
