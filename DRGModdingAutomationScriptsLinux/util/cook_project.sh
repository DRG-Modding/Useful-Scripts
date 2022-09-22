#!/bin/bash

. ./.env

echo -e "\n-> Cooking EU4 project at '$PROJECT_FILE'\n"

$WINE "$UE4_PATH/Engine/Binaries/Win64/UE4Editor-Cmd.exe" "Z:$PROJECT_FILE" -run=cook -targetplatform=WindowsNoEditor

WINE_ERROR=$?

if [ $WINE_ERROR -ne 0 ]; then
    echo -e "\n-x Error while cooking the project\n"
    exit $WINE_ERROR
fi

echo -e "\n== Cooking EU4 project done ==\n"
