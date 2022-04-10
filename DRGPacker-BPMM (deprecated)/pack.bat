@echo off
setlocal enableextensions enabledelayedexpansion

:: Paths
set /p UE_version=<.UE_version.txt
set UE_path="C:\Program Files\Epic Games\UE_%UE_version%"
set input=.input.txt
set log=.UnrealPak.log

:: UnrealPak project input (comment out 'del %input%' to see what was written)
echo "%cd%\input\" "../../../FSD/"> %input%


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


%UE_path%\Engine\Binaries\Win64\UnrealPak.exe "%cd%\new_P.pak" -Create="%cd%\%input%" -compress > %log% & type %log%

del %input%

(type %log% | findstr /i /c:"Error" >nul) && ( 
	del %log%
	echo.
	echo ERROR: PACKING FAILED - please check %log% in %cd%\ for details
	pause
	exit /b 1
) || ( 
	del %log%
	echo Packing done.
	if "%1"=="" ( pause )
)
