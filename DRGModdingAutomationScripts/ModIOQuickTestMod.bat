@echo off
setlocal EnableDelayedExpansion

::Set active directory to the dir the bat is in
pushd %~dp0

call VerifyVars.bat noPause

::Find variables in config.ini
for /f "tokens=1,2 delims==" %%g in (Config.ini) do (
	if %%g==SteamInstall set SteamInstall=%%h
	if %%g==ModName set ModName=%%h
)

call CookUEProject.bat noPause

call PackageMod.bat noPause

REM mkdir "%SteamInstall%\FSD\Mods\%ModName%"

REM echo removing old mod pak
REM del "%SteamInstall%\FSD\Mods\%ModName%\*" /q

REM echo copying over new mod pak
REM move "%cd%\Temp\%ModName%.pak" "%SteamInstall%\FSD\Mods\%ModName%\"

echo uploading to mod.io
"%cd%\ModIOUpload.bat" noPause UseTempPak
pause
