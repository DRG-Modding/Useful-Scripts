@echo off
echo.

:: Paths
set DRG_packaged_path=..\..\WindowsNoEditor\FSD\Content\_ModBPs
set packer=.
set input=%packer%\input\Content\_ModBPs

:: Check cmd parameters
set modID="%1"
if %modID%=="" (
	echo This script packages your BPMM mod, moves it to the DRG paks dir and runs the game
	echo.
	echo Usage: autopipelineBPMM.bat BMPP_mod_ID [wait_for_UE]
	echo 	If wait_for_UE is set to any value, the script will delete _ModBPs and wait for UE to repackage them
	echo 	Otherwise, the script will use the existing values
	pause
	exit /b 1 
)

:: Wait for UE to complete packaging
if not "%2"=="" (
	echo Deleting %DRG_packaged_path%
	rmdir /s /q %DRG_packaged_path%

	@echo off
	echo.
	echo Waiting for UE packaging...
	:waitloop
	IF EXIST %DRG_packaged_path% GOTO waitloopend
	C:\Windows\System32\ping -n 2 127.0.0.1 > nul
	goto waitloop
	: waitloopend
	rem :: does nothing, but script errors otherwise
)

@echo on
C:\Windows\System32\xcopy /E /I /Y "%DRG_packaged_path%" "%input%"
@echo off
if ERRORLEVEL 1 (
	echo.
	echo ERROR: copy of packaged files failed! 
	echo 	In UE editor, run packaging in the folder "%cd%\..\..\"
	pause
	exit /b ERRORLEVEL
)
attrib +r %input%\Mod%modID%.*
del /q %input%\* > nul 2>&1
attrib -r %input%\*

call %packer%\pack_and_install.bat 0
if ERRORLEVEL 1 (
	echo ERROR: pack_and_install failed!
	exit /b ERRORLEVEL
)

echo Launching game...
"C:\Program Files (x86)\Steam\steam" steam://rungameid/548430