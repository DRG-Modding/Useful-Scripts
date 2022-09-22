#!/bin/bash

. ./.env

DO_COOK=1
DO_PACK=1

Help()
{
   echo "Prepares the mod for release."
   echo "Cooks and packs the mod, then creates a zip to be uploaded to mod.io."
   echo
   echo "Syntax: $0 [-h|c|p]"
   echo "options:"
   echo "h     Shows this help."
   echo "c     Disable cooking."
   echo "p     Disable packing."
   echo
}


while getopts ":hcp" option; do
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
        \?) # Invalid option
         echo "Error: Invalid option $option"
         echo
         Help
         exit;;
    esac
done

echo -e "\n-> Preparing mod for release\n"

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

read -e -p "Please enter a suffix for this release: " RELEASE_SUFFIX

echo "Zipping the mod"
zip $MOD_NAME$RELEASE_SUFFIX.zip $MOD_NAME.pak

echo -e "\n== Mod preparation done ==\n"

