// Copyright Epic Games, Inc. All Rights Reserved.

#include "AssetGenerator.h"

static const FName AssetGeneratorTabName("AssetGenerator");

#define LOCTEXT_NAMESPACE "FAssetGeneratorModule"

void FAssetGeneratorModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FAssetGeneratorStyle::Initialize();
	FAssetGeneratorStyle::ReloadTextures();

	FAssetGeneratorCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FAssetGeneratorCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FAssetGeneratorModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FAssetGeneratorModule::RegisterMenus));
}

void FAssetGeneratorModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FAssetGeneratorStyle::Shutdown();

	FAssetGeneratorCommands::Unregister();
}

void FAssetGeneratorModule::PluginButtonClicked()
{
	// Does user wish to run first or second operation?
	if (Utils::GetSelectedButtonFromDialog("Do you wish to run asset generator first?", EAppMsgType::YesNo,
	                                       EAppReturnType::Yes))
	{
		Utils::OpenMessageDialog(EAppMsgType::Ok, "Running asset generator operation.");

		// Run asset generator operation
		if (OpenDialogMenu())
		{
			AssetGenOperation::ParseJSON(LoadFile());
		}
		
		// Allow user to cancel next operation
		if (Utils::GetSelectedButtonFromDialog(R"(Successfully finished creation of assets in given locations.
			Do you wish to continue to the next operation?)", EAppMsgType::OkCancel, EAppReturnType::Cancel))
		{
			Utils::OpenMessageDialog(EAppMsgType::Ok, "Cancelled the next operation.");
		} else
		{
			Utils::OpenMessageDialog(EAppMsgType::Ok, "Running stub filler operation.");
	
			// Run stub filler operation
		}
	} else
	{
		Utils::OpenMessageDialog(EAppMsgType::Ok, "Running stub filler operation.");
		
		// Run stub filler operation
	}
}

void FAssetGeneratorModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FAssetGeneratorCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("Settings");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FAssetGeneratorCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

bool FAssetGeneratorModule::OpenDialogMenu()
{
	IDesktopPlatform* FileManager = FDesktopPlatformModule::Get();
	FileManager->OpenFileDialog(0, DialogName, DefaultPath, DefaultFile, FileTypes, Flags,SelectedFileNames);
	if (SelectedFileNames.Num() > 1 && !FileManager)
	{
		UE_LOG(LogTemp, Error, TEXT("FileManipulation: Please only select one file!"));
		return false;
	}
	UE_LOG(LogTemp, Display, TEXT("FileManipulation: File %s loaded."), *SelectedFileNames[0]);
	return true;
}

FString FAssetGeneratorModule::LoadFile()
{
	IPlatformFile& FileManager = FPlatformFileManager::Get().GetPlatformFile();
	FString FileContent;
	if (FileManager.FileExists(*SelectedFileNames[0]))
	{
		if (FFileHelper::LoadFileToString(FileContent, *SelectedFileNames[0], FFileHelper::EHashOptions::None))
		{
			UE_LOG(LogTemp, Display, TEXT("FileManipulation: Text From File: %s"), *FileContent);
		} else
		{
			UE_LOG(LogTemp, Error, TEXT("FileManipulation: Could not load text from file for some reason."));
		}
	} else
	{
		UE_LOG(LogTemp, Error, TEXT("FileManipulation: Could not read file because it was not found."));
		UE_LOG(LogTemp, Error, TEXT("FileManipulation: Expected file location: %s"), *SelectedFileNames[0]);
	}
	return FileContent;
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FAssetGeneratorModule, AssetGenerator)