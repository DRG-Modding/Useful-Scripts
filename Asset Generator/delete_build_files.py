import os

FILE_PATH = "F:\DRG Modding\Project Generator\FSDTemplateU36P4"

for root, dirs, files in os.walk(FILE_PATH):
    for name in dirs:
        if name == "Binaries" or name == "Intermediate":
            os.remove(os.path.join(root, name))
            # Delete all files in directory
            for file in os.listdir(os.path.join(root, name)):
                os.remove(os.path.join(root, name, file))
            print("Deleted: " + os.path.join(root, name))
        else:
            print("Skipped: " + os.path.join(root, name))