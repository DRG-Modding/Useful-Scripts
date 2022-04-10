@echo off
setlocal enabledelayedexpansion

:: Paths
set unpacked="%cd%\unpacked"
set /p UE_version=<.UE_version.txt
set UE_path="C:\Program Files\Epic Games\UE_%UE_version%"

:: Validate UE_path, try Program Files (x86)
IF NOT EXIST !UE_path! (
	echo !UE_path!
	set UE_path="C:\Program Files (x86)\Epic Games\UE_%UE_version%"
	IF NOT EXIST !UE_path! (
		echo "ERROR: Epic Games install directory not found (!UE_path!) Please set variable UE_path manually." 1>&2
		pause
		exit /b 1
	)
)

if exist %unpacked% (
	rmdir /s /q %unpacked%
)


%UE_path%\Engine\Binaries\Win64\UnrealPak.exe %1 -extract "%unpacked%"

pause