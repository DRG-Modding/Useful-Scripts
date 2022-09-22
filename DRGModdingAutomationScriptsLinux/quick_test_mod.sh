#!/bin/bash

. ./.env


DO_COOK=1
DO_PACK=1
DO_GAME=1

Help()
{
   echo "Cooks and packs the mod, then installs it in DRG."
   echo
   echo "Syntax: $0 [-h|c|p|g]"
   echo "options:"
   echo "h     Shows this help."
   echo "c     Disable cooking."
   echo "p     Disable packing."
   echo "g     Disable starting the game."
   echo
}


while getopts ":hcpg" option; do
    case $option in
        h) # display Help
            Help
            exit;;
        c) # Disable cooking
            echo "Skipping cook phase"
            DO_COOK=0;;
        p) # Disable packing
            echo "Skipping pack phase"
            DO_PACK=0;;
        g) # Disable starting the game
            echo "Skipping game launching phase"
            DO_GAME=0;;
        \?) # Invalid option
         echo "Error: Invalid option $option"
         echo
         Help
         exit;;
    esac
done

echo -e "\n-> Installing mod for testing\n"

if [ $DO_COOK -ne 0 ]; then
    ./util/cook_project.sh
    COOK_ERROR=$?
    if [ $COOK_ERROR -ne 0 ]; then
        exit $COOK_ERROR
    fi
fi
if [ $DO_PACK -ne 0 ]; then
    ./util/pack_project.sh
    PACK_ERROR=$?
    if [ $PACK_ERROR -ne 0 ]; then
        exit $PACK_ERROR
    fi
fi

MOD_INSTALL_DIR="$DRG_PATH/FSD/Mods/$MOD_NAME"

echo "Installing the mod"
# Clean the folder to make sure only the mod is there
rm -r "$MOD_INSTALL_DIR"
mkdir -p "$MOD_INSTALL_DIR"
cp "$MOD_NAME.pak" "$MOD_INSTALL_DIR"

echo "Cleaning up after install"
rm "$MOD_NAME.pak"

echo -e "\n== Mod installation done ==\n"

if [ $DO_GAME -ne 0 ]; then
    echo -e "Starting DRG...\n"
    steam steam://rungameid/548430
fi
