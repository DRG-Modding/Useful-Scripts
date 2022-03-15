@echo off
if "%~1"=="" goto skip

setlocal enableextensions
pushd %~dp0
".\UnrealPak\Engine\Binaries\Win64\UnrealPak.exe" %1 -platform="Windows" -extract "%CD%\%~n1"
popd
pause

:skip