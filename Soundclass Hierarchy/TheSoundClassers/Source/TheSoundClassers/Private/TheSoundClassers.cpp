// Copyright Epic Games, Inc. All Rights Reserved.

#include "TheSoundClassers.h"
#include "TheSoundClassersStyle.h"
#include "TheSoundClassersCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"

#include "DesktopPlatform/Public/IDesktopPlatform.h"
#include "DesktopPlatform/Public/DesktopPlatformModule.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"	
#include "UObject/UObjectGlobals.h"

static const FName TheSoundClassersTabName("TheSoundClassers");

#define LOCTEXT_NAMESPACE "FTheSoundClassersModule"

void FTheSoundClassersModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FTheSoundClassersStyle::Initialize();
	FTheSoundClassersStyle::ReloadTextures();

	FTheSoundClassersCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FTheSoundClassersCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FTheSoundClassersModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FTheSoundClassersModule::RegisterMenus));
}

void FTheSoundClassersModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FTheSoundClassersStyle::Shutdown();

	FTheSoundClassersCommands::Unregister();
}

void FTheSoundClassersModule::PluginButtonClicked()
{
	TArray<FString> outFileNames;
	FString dialogName = "Hi";
	FString defaultPath = "C:";
	FString defaultFile = "";
	FString fileTypes = ".txt";
	uint32 flags = 0;

	//FPackageName::RegisterMountPoint("/MyMountPoint/", FPaths::EnginePluginsDir());

	IDesktopPlatform* fpl = FDesktopPlatformModule::Get();
	fpl->OpenFileDialog(0, dialogName, defaultPath, defaultFile, fileTypes, flags, outFileNames);

	TSharedPtr<MyNodeClass> myFileParser = ConfigParser(outFileNames[0]);
	myFileParser->ConstructChildren();

	// Put your "OnButtonClicked" stuff here
	FText DialogText = LOCTEXT("PluginButtonDialogText", "The Music Hierachy has finished.");
	FMessageDialog::Open(EAppMsgType::Ok, DialogText);
}

void FTheSoundClassersModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FTheSoundClassersCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("Settings");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FTheSoundClassersCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}


TSharedPtr<MyNodeClass> FTheSoundClassersModule::ConfigParser(FString FileLocation) {
	IPlatformFile& FileManager = FPlatformFileManager::Get().GetPlatformFile();
	FString FileContent;
	TArray<FString> LineArray;
	if (FileManager.FileExists(*FileLocation))
	{
		// We use the LoadFileToString to load the file into
		if (FFileHelper::LoadFileToString(FileContent, *FileLocation, FFileHelper::EHashOptions::None))
		{
			UE_LOG(LogTemp, Warning, TEXT("FileManipulation: Text From File: %s"), *FileContent);
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("FileManipulation: Did not load text from file"));
		}
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("FileManipulation: ERROR: Can not read the file because it was not found."));
		UE_LOG(LogTemp, Warning, TEXT("FileManipulation: Expected file location: %s"), *FileLocation);
	}
	FileContent.RemoveSpacesInline();
	FileContent.ParseIntoArrayLines(LineArray);


	TSharedPtr<MyNodeClass> ReturnNodes = MakeShared<MyNodeClass>(MyNodeClass(LineArray[0], 0));
	ReturnNodes->ParseConfig(&LineArray, 0);
	return ReturnNodes;
}



#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FTheSoundClassersModule, TheSoundClassers)