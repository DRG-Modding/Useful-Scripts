@echo off

if not exist Config.ini (
	echo making default config
	copy nul Config.ini
	(
		echo ProjectFile=..\FSD\FSD.uproject
		echo UnrealEngineLocation=C:\Program Files ^(x86^)\UE_4.25\
		echo ModName=myMod
		echo SteamInstall=C:\Program Files ^(x86^)\Steam\steamapps\common\Deep Rock Galactic\
	) > Config.ini
)

if not exist PakWhiteList.ini (
	echo making default PakWhiteList
	copy nul PakWhiteList.ini
	(
		echo ..\Content
		echo ..\AssetRegistry.bin
	) > PakWhiteList.ini
)

if not exist PakBlackList.ini (
	echo making default PakBlackList
	copy nul PakBlackList.ini
	
)
if not exist ModIOConfig.ini (
	echo making ModIOConfig
	copy nul ModIOConfig.ini
	(
		echo Token=
		echo ModID=
		echo MajorVersion=1
		echo MinorVersion=0
		echo AutoIncrementVersion=true
		echo AddVersionToModName=true
		echo AskForChangelog=true
		echo Changelog=
		echo Verbose=false
		echo GameID=2475
		echo ZipLocation=.
		echo LastZip=
		echo LastPak=
	) > ModIOConfig.ini
)
