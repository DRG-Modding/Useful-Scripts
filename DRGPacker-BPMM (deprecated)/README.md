# General
These scripts allow unpacking .pak files and packing your project into a new .pak.

They automatically detect the UE path (assuming default install locations) and use the current working directory, so they are ready for use with no changes needed (using the default [DRG-modding](https://github.com/DRG-Modding/DRG-Modding) repository layout)!

## Requirements
* Unreal Engine installed to `C:\Program Files\Epic Games\UE_*\` or `C:\Program Files (x86)\Epic Games\UE_*\`.
* In UE, the packaging target directory must be selected to be the root of the [DRG-modding](https://github.com/DRG-Modding/DRG-Modding) repository (your files should be packaged into the already present ´WindowsNoEditor/´ directory). This can be changed in ´autopipeline.bat´.

# unpack.bat
Pass the .pak file to be unpacked as an argument (or drag it onto unpack.bat)
Contents will be unpacked into `./unpacked/`

# pack.bat
Place your files in input/ and run.

# pack_and_install.bat
Runs `pack.bat` and moves the mod to DRG Content/paks directory.

# autopipeline.bat
This script allows for the highest level of automation:

## Usage 1 - your files are already packaged by UE
Pass as the first argument your BPMM mod ID (e.g. 069) OR your native mod name (e.g. MyTestMod), which must also be the name of your mod directory under `Content/`. 

The script will automatically copy packaged mod files from `../../WindowsNoEditor/FSD/Content/_ModBPs` to `./input/`, run `pack_and_install.bat` and launch the game for testing.

## Usage 2 - UE has not yet finished packaging your mod
Pass as the first argument your BPMM mod ID or native mod name and anything as the second argument (e.g. "0").

First, the script will wait for UE packaging to complete (into `../../WindowsNoEditor/`) and then run the same sequence of actions as in Usage 1.

## IMPORTANT: Files copied to `input/`:
* BPMM mods: any from `_ModBPs/` that contain the given mod ID in their filename *and* all files that don't have any ID in their filename.
* Native mods: the directory matching the given mod name.

Any other files that your mod requires should be placed in the `input/` directory before running the script.

## Note
	Create a shortcut to run the script with fixed parameters by adding them to the Target in the shortcut's file properties.
