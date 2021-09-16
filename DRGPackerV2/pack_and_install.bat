:: Does not modify input/ dir, just moves new_P.pak to DRG paks

@echo off
set fn=new_P.pak

call pack.bat 0
if ERRORLEVEL 1 (
	echo ERROR: Packing failed
	exit /b ERRORLEVEL
)

move %fn% "C:\Program Files (x86)\Steam\steamapps\common\Deep Rock Galactic\FSD\Content\Paks" > nul

if ERRORLEVEL 1 (
	echo ERROR: Failed to move %fn% to game paks directory! Is the game running?
	exit /b ERRORLEVEL
) else (
	echo Pack and install done.
	if "%1"=="" ( pause )
)