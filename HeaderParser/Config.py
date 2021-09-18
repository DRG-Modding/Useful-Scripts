import shutil
from conflicts import move_conflicts
from Parser import DumpSelfVars


class Config(DumpSelfVars):

    def __init__(self):
        # main.py options
        self.ORIGINALS_DIR = "../../Header-Dumps/U34.5/DUMP/"
        self.WORKING_DIR = "Headers"
        self.CONFLICT_DIR = "Headers_conflict"
        self.OUTPUT_DIR = "Headers_parsed"
        self.TEMPLATE_DIR = "Templates"
        self.RELOAD = False
        self.FETCH_AFTER_RUN = True

        # fetch_class.py options
        self.FETCH_DIR = "Headers_fetched"
        self.FETCH_INTO_SUBDIRS = False
        self.CLEAR_BEFORE_FETCH = True
        self.AUTOFETCH = ["AfflictionEffect"]

    def reload(self):
        """
        1. Clear WORKING_DIR and CONFLICT_DIR
        2. Load header files from ORIGINALS_DIR
        3. Move headers present in UE4 source code to CONFLICT_DIR
        """
        print("Removing old header files.")
        shutil.rmtree(self.WORKING_DIR, True)
        shutil.rmtree(self.CONFLICT_DIR, True)
        print(f"Copying new files from '{self.ORIGINALS_DIR}'... ", end="")
        shutil.copytree(self.ORIGINALS_DIR, self.WORKING_DIR)
        print("OK!\n")
        move_conflicts(self.WORKING_DIR, self.CONFLICT_DIR)
        print()
