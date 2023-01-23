import os
import subprocess
import re
import datetime
import shutil
from uuid import uuid4

EDITOR_EXE= r"F:/UNEPIC GAMES/UE_4.27/Engine/Binaries/Win64/UE4Editor-Cmd.exe"
UBT_EXE = r"F:/UNEPIC GAMES/UE_4.27/Engine/Binaries/DotNET/UnrealBuildTool.exe"
PROJECT_GEN_UPROJECT = r"F:/DRG Modding/Project Generator/UE4GameProjectGenerator4.27/GameProjectGenerator.uproject"
HEADER_DUMP = r"C:/Program Files (x86)/Steam/steamapps/common/Deep Rock Galactic/FSD/Binaries/Win64/UHTHeaderDump"
PROJECT_FILE = r"F:/DRG Modding/DRGPacker/_unpacked/FSD/FSD.uproject"
PLUGIN_MANIFEST = r"F:/DRG Modding/DRGPacker/_unpacked/FSD/Plugins/FSD.upluginmanifest"
OUTPUT_DIR_START = r"F:/DRG Modding/Project Generator"
MODIO_SOURCES_DIR = r"F:/DRG Modding/Project Generator/Modio"
GITHUB_REPO = r"F:/Github Projects/Other/DRG Modding Org/FSD-Template"

def check_drive_space():
    _, _, free = shutil.disk_usage(os.path.splitdrive(OUTPUT_DIR_START)[0])
    free = free // (2 ** 30)
    if free < 25:
        print("Not enough space on drive to run generator - needs at least 25GB")
        return False
    return True

def get_project_name():
    uuid = str(uuid4()).replace("-", "")
    uuid = re.sub(r"\d", "", uuid)
    return uuid[:8]

def run_project_gen(name):
    print("============================================================")
    print("               RUNNING PROJECT GENERATOR                    ")
    print("============================================================")
    os.mkdir(os.path.join(OUTPUT_DIR_START, name))
    subprocess.run([
        EDITOR_EXE, 
        PROJECT_GEN_UPROJECT,
        "-run=ProjectGenerator",
        "-HeaderRoot=" + HEADER_DUMP,
        "-ProjectFile=" + PROJECT_FILE,
        "-PluginManifest=" + PLUGIN_MANIFEST,
        "-OutputDir=" + os.path.join(OUTPUT_DIR_START, name),
        "-stdout",
        "-unattended",
        "-NoLogTimes"
    ])

def copy_modio_sources(name):
    print("============================================================")
    print("                COPYING MOD.IO SOURCE CODE                  ")
    print("============================================================")
    # Delete the folder called Modio inside of OutputDir/Plugins
    os.system(
        "rmdir " + 
        '"' + 
        os.path.join(OUTPUT_DIR_START, name, "Plugins", "Modio") + 
        '"' + 
        " /S /Q"
    )

    # Copy the new sources from Modio Source to template/Plugins/Modio
    subprocess.run([
        "xcopy", 
        MODIO_SOURCES_DIR,
        os.path.join(OUTPUT_DIR_START, name, "Plugins", "Modio"),
        "/E",
        "/I",
        "/Y"
    ])

def change_lines(file_name, line_num, text, is_replace, is_regex = False, match_group = ""):
    if not os.path.exists(file_name): return
    lines = open(file_name, 'r').readlines()

    if is_regex:
        for i, line in enumerate(lines):
            if re.search(text, line):
                lines[i] = re.sub(text, match_group, line)
                print("Replaced line " + str(i) + " with " + match_group + " in " + file_name)
    else:
        if is_replace: lines[line_num] = text
        else: lines.insert(line_num, text)
        print("Replaced line " + str(line_num) + " with " + text + " in " + file_name)
    
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def modify_project_file(proj_name, file_name, line_number, is_replace, text, accessor = "Public", module = "FSD", is_regex = False, match_group = ""):
    open_module = os.path.join(OUTPUT_DIR_START, proj_name, "Source", module)
    if is_regex:
        change_lines(file_name, line_number, text, is_replace, is_regex, match_group)
    else:
        change_lines(os.path.join(open_module, accessor, file_name), line_number, text, is_replace)

def run_rules(name):
    print("============================================================")
    print("                RUNNING THROUGH FIX RULES                   ")
    print("============================================================")

    # CharacterSightSensor.h
    modify_project_file(name, "CharacterSightSensor.h", 7, False, "DECLARE_DYNAMIC_MULTICAST_DELEGATE(FCharacterSightSensorDelegate);\n")
    modify_project_file(name, "CharacterSightSensor.h", 8, False, "\n")

    # FSDProjectileMovementComponent.h
    modify_project_file(name, "FSDProjectileMovementComponent.h", 9, False, "DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnProjectilePenetrateDelegate);\n")
    modify_project_file(name, "FSDProjectileMovementComponent.h", 10, False, "DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnProjectileOutOfPropulsion);\n")
    modify_project_file(name, "FSDProjectileMovementComponent.h", 11, False, "\n")

    # SubHealthComponent.h, line 56
    modify_project_file(name, "SubHealthComponent.h", 55, True, "\t//UFUNCTION(BlueprintCallable)\n")

    # HealthComponentBase.h, line 117
    modify_project_file(name, "HealthComponentBase.h", 116, True, "\t//UFUNCTION(BlueprintCallable)\n")

    # HealthComponent.h, line 98
    modify_project_file(name, "HealthComponent.h", 97, True, "\t//UFUNCTION(BlueprintCallable)\n")

    # EnemyHealthComponent.h, line 39
    modify_project_file(name, "EnemyHealthComponent.h", 38, True, "\t//UFUNCTION(BlueprintCallable)\n")

    # FriendlyHealthComponent.h, line 33
    modify_project_file(name, "FriendlyHealthComponent.h", 32, True, "\t//UFUNCTION(BlueprintCallable)\n")

    # ShowroomStage.cpp, line 16
    modify_project_file(name, "ShowroomStage.cpp", 15, True, '\t//this->SceneCapture = CreateDefaultSubobject<USceneCaptureComponent2D>(TEXT("SceneCapture"));\n', "Private")

    # GameFunctionLibrary.cpp, line 46
    modify_project_file(name, "GameFunctionLibrary.cpp", 45, True, '\treturn true;\n', "Private")

    # Search every file in both modules and accessors for the following regex string: (const) ((\w+)\*\&) and replace it with $2
    for root, _, files in os.walk(os.path.join(OUTPUT_DIR_START, name, "Source")):
        for file in files:
            if file.endswith(".h") or file.endswith(".cpp"):
                modify_project_file(name, os.path.join(root, file), 0, False, "(const) ((\w+)\*\&)", "", "", True, r"\2")

def generate_build_files(name):
    # Running F:/UNEPIC GAMES/UE_4.27/Engine/Binaries/DotNET/UnrealBuildTool.exe  -projectfiles -project="F:/DRG Modding/Project Generator/Test1/FSD.uproject" -game -rocket -progress -log="F:\DRG Modding\Project Generator\Test1/Saved/Logs/UnrealVersionSelector-2023.01.23-14.49.22.log"
    print("============================================================")
    print("                    GENERATING BUILD FILES                  ")
    print("============================================================")
    date = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    subprocess.run([
        UBT_EXE,
        "-projectfiles",
        "-project=" + os.path.join(OUTPUT_DIR_START, name, "FSD.uproject"),
        "-game",
        "-rocket",
        "-progress",
        "-log=" + os.path.join(OUTPUT_DIR_START, name, "Saved/Logs/UnrealVersionSelector-" + str(date) + ".log")
    ])

def compile_project(name):
    # Running F:/UNEPIC GAMES/UE_4.27/Engine/Binaries/DotNET/UnrealBuildTool.exe Development Win64 -Project="F:/DRG Modding/Project Generator/0bf3519b-552a-451d-8ecc-5d72269dea65/FSD.uproject" -TargetType=Editor -Progress -NoEngineChanges -NoHotReloadFromIDE
    print("============================================================")
    print("                    COMPILING PROJECT                       ")
    print("============================================================")
    subprocess.run([
        UBT_EXE,
        "Development",
        "Win64",
        "-Project=" + os.path.join(OUTPUT_DIR_START, name, "FSD.uproject"),
        "-TargetType=Editor",
        "-Progress",
        "-NoEngineChanges",
        "-NoHotReloadFromIDE"
    ])

def copy_template_to_repo(name):
    print("============================================================")
    print("               COPYING TEMPLATE TO GITHUB REPO              ")
    print("============================================================")
    # First, delete the following folders in the GITHUB_REPO folder: Binaries, Plugins, Source, Saved, Intermediate, FSD.sln, FSD.uproject
    # Check that they exist first
    files_to_delete = ["Binaries", "Plugins", "Source", "Saved", "Intermediate", "FSD.sln", "FSD.uproject"]
    files_to_copy = ["Binaries", "Plugins", "Source", "FSD.sln", "FSD.uproject"]
    for file in files_to_delete:
        if os.path.exists(os.path.join(GITHUB_REPO, file)):
            if os.path.isfile(os.path.join(GITHUB_REPO, file)): os.remove(os.path.join(GITHUB_REPO, file))
            else: shutil.rmtree(os.path.join(GITHUB_REPO, file))
            print("Deleted " + file)
    
    # Copy the template to the GITHUB_REPO folder
    for file in files_to_copy:
        file_path = os.path.join(OUTPUT_DIR_START, name, file)
        if os.path.exists(file_path):
            if os.path.isfile(file_path): shutil.copyfile(file_path, os.path.join(GITHUB_REPO, file))
            else: shutil.copytree(file_path, os.path.join(GITHUB_REPO, file))
            print("Copied " + file)

def main():
    if not check_drive_space(): return
    name = get_project_name()
    run_project_gen(name)
    copy_modio_sources(name)
    run_rules(name)
    generate_build_files(name)
    compile_project(name)
    copy_template_to_repo(name)

if __name__ == "__main__":
    main()