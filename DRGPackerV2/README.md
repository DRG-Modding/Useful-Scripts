# General
These scripts allow unpacking .pak files and packing your project into a new .pak.

They automatically detect the UE path (assuming default install locations) and use the current working directory, so they are ready for use with no changes needed (using the default repository layout)!
In UE, the packaging target directory should be selected to be the root of the repo.

## Requirements
Unreal Engine installed to `C:\Program Files\Epic Games\UE_*\` or `C:\Program Files (x86)\Epic Games\UE_*\`.

# unpack.bat
Pass the .pak file to be unpacked as an argument (or drag it onto unpack.bat)
Contents will be unpacked into `./unpacked/`

# pack.bat
Place your files in input/ and run.

# pack_and_install.bat
Runs `pack.bat` and moves the mod to DRG Content/paks directory.

# autopipelineBPMM.bat
This script allows for the highest level of automation:
## Usage 1
	Pass as the first argument your BPMM mod ID (e.g. 069). 
	The script will automatically copy packaged mod files (for the given BPMM mod ID) from `../../WindowsNoEditor/FSD/Content/_ModBPs` to `./input/`, run `pack_and_install.bat` and launch the game for testing.
## Usage 2
	Pass as the first argument your BPMM mod ID and anything as the second argument (e.g. "0").
	First the script will wait for UE packaging to complete (into `../../WindowsNoEditor/`) and then run the same sequence of actions as in Usage 1.
## IMPORTANT
	This script does NOT copy any files from the `..\..\WindowsNoEditor\FSD\Content\` directory other than the `_ModBPs` directory! If your BPMM mod uses any files outside `_ModBPs`, then you have to copy them to `./input/` manually before running the script!
## Note
	Create a shortcut to run the script with fixed parameters by adding them to the Target in the shortcut's file properties.
