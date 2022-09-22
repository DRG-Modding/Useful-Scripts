#!/bin/bash

. ./.env

echo -e "\n-> Setting up EU4 project at '$PROJECT_FILE'\n"

$WINE "$UE4_PATH/Engine/Binaries/DotNET/UnrealBuildTool.exe" -projectfiles -project="Z:$PROJECT_FILE" -game -rocket -progress

echo -e "\n== Setting up EU4 project done ==\n"
