// Copyright Epic Games, Inc. All Rights Reserved.

#include "AssetGenerator.h"
#include "AssetGeneratorStyle.h"
#include "AssetGeneratorCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"

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
	FText DialogText = FText::Format(LOCTEXT("PluginButtonDialogText", "Do you wish to run asset generator first?"));
	if (FMessageDialog::Open(EAppMsgType::YesNo, DialogText) == EAppReturnType::Yes)
	{
		DialogText = FText::Format(LOCTEXT("PluginButtonDialogText", "Running asset generator operation."));
		FMessageDialog::Open(EAppMsgType::Ok, DialogText);

		// Run asset generator operation
		
		
		// Show success of asset generation
		DialogText = FText::Format(
								LOCTEXT("PluginButtonDialogText", "Successfully finished creation of {0} assets in given locations.{1}"),
								AssetNames.Max(),
								FText::FromString(TEXT("\nDo you wish to continue to the next operation?")));
		
		// Allow user to cancel next operation
		if (FMessageDialog::Open(EAppMsgType::OkCancel, DialogText) == EAppReturnType::Cancel)
		{
			DialogText = FText::Format(LOCTEXT("PluginButtonDialogText", "Cancelled the next operation."));
			FMessageDialog::Open(EAppMsgType::Ok, DialogText);
		} else
		{
			DialogText = FText::Format(LOCTEXT("PluginButtonDialogText", "Running stub filler operation."));
			FMessageDialog::Open(EAppMsgType::Ok, DialogText);

			// Run stub filler operation
		}
	} else
	{
		DialogText = FText::Format(LOCTEXT("PluginButtonDialogText", "Running stub filler operation."));
		FMessageDialog::Open(EAppMsgType::Ok, DialogText);

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

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FAssetGeneratorModule, AssetGenerator)