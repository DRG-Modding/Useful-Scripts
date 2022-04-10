@echo off
echo.

:: Paths
set packaged_content_path=..\..\WindowsNoEditor\FSD\Content
set packer_path=.
set input_content_path=%packer_path%\input\Content
set game_path="C:\Program Files (x86)\Steam\steamapps\common\Deep Rock Galactic\FSD"
set xcopy=C:\Windows\System32\xcopy

set "echo_nl=echo | set /p _="
set "echo_on=echo on&for %%. in (.) do"
set "prmpt=Prompt $G  "

:: Check cmd parameter
set modID="%1"
if %modID%=="" ( goto print_help )

SET "native="&for /f "delims=0123456789" %%i in ("%1") do set native=%%i
if defined native (echo %modID% - NOT numeric - detected NATIVE mod) else (echo %modID% - numeric - detected BPMM mod)


:: Wait for UE to complete packaging
if not "%2"=="" (
	echo Deleting %packaged_content_path%
	rmdir /s /q %packaged_content_path%

	echo.
	echo Waiting for UE packaging...
	:waitloop
	IF EXIST %packaged_content_path% GOTO waitloopend
	C:\Windows\System32\ping -n 2 127.0.0.1 > nul
	goto waitloop
	: waitloopend
	rem :: does nothing, but script errors otherwise
)

:: Check if mod exists and copy mod files to input
echo.&echo.&%echo_nl% Copying UE packaged files...
if defined native (
	if not exist %packaged_content_path%\%modID%\ (
		echo ERROR: mod with name '%modID%' not found at %packaged_content_path%\%modID%\
		pause
		exit /b 1
	)
	%prmpt%
	%echo_on% %xcopy% /Y %packaged_content_path%\..\AssetRegistry.bin %input_content_path%\..\ > nul
	@if ERRORLEVEL 1 goto asset_registry_copy_error
	%echo_on% %xcopy% /E /I /Y %packaged_content_path%\%modID% %input_content_path%\%modID% > nul
) else (
	if not exist %packaged_content_path%\_ModBPs\Mod%modID%.* (
		echo ERROR: BPMM mod with ID %modID% not found in %packaged_content_path%\_ModBPs\
		pause
		exit /b 1
	)
	%prmpt%
	%echo_on% %xcopy% /E /I /Y %packaged_content_path%\_ModBPs %input_content_path%\_ModBPs > nul
)

@echo off
Prompt
if ERRORLEVEL 1 goto packaged_file_copy_error

:: BPMM mods: remove other mods and install
echo.&echo.&%echo_nl%Packing and installing... 
%prmpt%
if not defined native (
	:: Remove all mod files which contain an ID other than modID in their name
	attrib +r %input_content_path%\_ModBPs\* /s
	attrib -r %input_content_path%\_ModBPs\Mod* /s
	attrib -r %input_content_path%\_ModBPs\???_* /s
	attrib +r %input_content_path%\_ModBPs\*%modID%* /s
	del /s /q %input_content_path%\_ModBPs\* > nul 2>&1
	attrib -r %input_content_path%\_ModBPs\* /s
	
	%echo_on% call %packer_path%\pack_and_install_BPMM.bat 0 > nul 
	Prompt &echo off
	
	if ERRORLEVEL 1 (
		echo ERROR: pack_and_install failed!
		exit /b ERRORLEVEL
	)
	
	:: cleanup BPMM files from input
	rmdir /q /s %input_content_path%\_ModBPs
	
	rem :: wtf batch-ass windows ") was unexpected at this time." why cant you be normal
) else ( :: Native mods: pack and install manually
	rem
	%echo_on% call pack.bat 0 > nul 
	echo off
	if ERRORLEVEL 1 (
		Prompt
		echo ERROR: Packing failed
		pause
		exit /b ERRORLEVEL
	)
	:: cleanup added mod files from input
	rmdir /q /s %input_content_path%\%modID%
	
	rmdir /q /s %game_path%\Mods\%modID%
	mkdir %game_path%\Mods\%modID%
	%echo_on% move %packer_path%\new_P.pak %game_path%\Mods\%modID%\%modID%.pak > nul
	Prompt &echo off
	if ERRORLEVEL 1 (
		echo ERROR: failed moving %packer_path%\new_P.pak to %game_path%\Mods\%modID%\%modID%.pak!
		pause
		exit /b ERRORLEVEL
	)
	rem
)

echo.&echo Launching game...
"C:\Program Files (x86)\Steam\steam" steam://rungameid/548430
exit /b 0


:print_help
	echo This script packages your BPMM or native loading mod, moves it to the DRG paks dir and runs the game
	echo.
	echo Usage: autopipelineBPMM.bat BMPP_ID_or_Mod_Name [wait_for_UE]
	echo 	If wait_for_UE is set to any value, the script will delete ..\..\WindowsNoEditor\FSD\Content\ 
	echo 		and wait for UE to regenerate the files from packaging
	echo 	Otherwise, the script will use the existing values
	pause
	exit /b 1 

:packaged_file_copy_error
	Prompt
	echo.
	echo ERROR: copy of packaged files failed! 
	echo 	In UE editor, run packaging in the folder "%cd%\..\..\"
	pause
	exit /b ERRORLEVEL

:asset_registry_copy_error
	@echo off
	Prompt
	echo.
	echo ERROR: copy of AssetRegistry.bin failed
	echo 	In UE editor, run packaging in the folder "%cd%\..\..\"
	pause
	exit /b ERRORLEVEL