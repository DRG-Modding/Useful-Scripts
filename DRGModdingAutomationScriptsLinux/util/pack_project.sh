#!/bin/bash

. ./.env

# VARIABLES SETUP -------------------------------

BAKED_PATH="$PROJECT_PATH/Saved/Cooked/WindowsNoEditor/FSD"
# Temporary folders used to pack the mod
TMP_WORKSPACE="$(pwd)/.tmp_pack"
TMP_WORKSPACE_INPUT="$TMP_WORKSPACE/input"
# Utility to convert Linux path to Windows
WINEPATH="$WINE"path
# Wine path to the resulting pak file
PAK_PATH="Z:$(pwd)/$MOD_NAME.pak"
# Wine path to the autogen file
AUTOGEN_PATH="Z:$TMP_WORKSPACE/autogen.txt"

# -----------------------------------------------

echo -e "\n-> Packing mod into $MOD_NAME.pak\n"

echo "Cleaning previous temporary directory"
rm -r "$TMP_WORKSPACE"
mkdir -p "$TMP_WORKSPACE"

echo "Copying assets to pack in temporary directory"
mkdir -p "$TMP_WORKSPACE_INPUT"
cp -r "$BAKED_PATH/Content" "$TMP_WORKSPACE_INPUT"
cp "$BAKED_PATH/AssetRegistry.bin" "$TMP_WORKSPACE_INPUT"

echo "Packing the mod"
echo "$($WINEPATH -w "$TMP_WORKSPACE_INPUT/*")" "../../../FSD/" > "$TMP_WORKSPACE/autogen.txt"

$WINE "$UE4_PATH/Engine/Binaries/Win64/UnrealPak.exe" "$PAK_PATH" -create="$AUTOGEN_PATH" -platform="Windows" -compress

WINE_ERROR=$?

echo "Cleaning up temporary directory after pack"
rm -r "$TMP_WORKSPACE"

if [ $WINE_ERROR -ne 0 ]; then
    echo -e "\n-x Error while cooking the project\n"
    exit $WINE_ERROR
fi


echo -e "\n== Packing done ==\n"
