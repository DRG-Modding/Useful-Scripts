@if "%~1"=="" goto skip

@setlocal enableextensions
@pushd %~dp0
@echo "%~1\*.*" "..\..\..\FSD\*.*" > input.txt
".\UnrealPak\Engine\Binaries\Win64\UnrealPak.exe" "%~1 _P.pak" -platform="Windows" -create="%CD%\input.txt" -compress
@popd
@pause

:skip