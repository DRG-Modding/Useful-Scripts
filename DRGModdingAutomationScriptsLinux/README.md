# DRG modding automation scripts - Linux

This repo contains various bash scripts to help you automate your projects, including packaging, zipping, cooking, and all those fun things.

Those scripts were inspired by the [bat scripts](https://github.com/DRG-Modding/Useful-Scripts/tree/main/DRGModdingAutomationScripts) by Samamstar but do not work exactly the same, so be sure to read this documentation first!

## Installation/usage

In order to use this I recommend downloading the repo and placing it on folder above your .uproject. By default the scripts use the parent folder name as the mod name, and expects your .uproject parent folder to be named `FSD`.

Imagine the following structure:

- My Mod
  - FSD
    - FSD.uproject

By placing the scripts under the `My Mod` folder, the project will be automatically detected and the scripts will use `My Mod` as the mod name.

The most useful scripts are:

- `quick_test_mod.sh`
  - Automatically runs all steps required to test mod locally, by cooking the project, packing it, copying it into the local mods folder, and automatically launching DRG through Steam. Use the `-h` option to see how to skip a specific step.
- `prep_mod_for_release.sh`
  - Automatically runs all steps required to upload to mod.io, including cooking the project, packing it and zipping up the pak. Use the `-h` option to see how to skip a specific step.
- `setup_cpp_project.sh`
  - If UE4 gives an error when trying to open a project with C++ headers, try using this script.

## Configuration

All the configuration is done through environnement variables in the `.env`. Open it and read the comments for each variable to understand how to fill the right values.

Some values are required, but some can be guessed from the folder in which the scripts are executed as explained in the `Installation/usage` section.
