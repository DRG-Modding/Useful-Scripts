// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AssetGenOperation.h"
#include "Misc/FileHelper.h"
#include "Modules/ModuleManager.h"

class FToolBarBuilder;
class FMenuBuilder;

class FAssetGeneratorModule : public IModuleInterface
{
public:
	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
	
	/** This function will be bound to Command. */
	void PluginButtonClicked();

	TArray<FString> SelectedFileNames;

private:
	void RegisterMenus();
	bool OpenDialogMenu();
	FString LoadFile();
	
	const FString& DialogName = "Open";
	const FString& DefaultPath = "C:";
	const FString& DefaultFile = "";
	const FString& FileTypes = ".json";
	const uint32 Flags = 0;
	
	TSharedPtr<class FUICommandList> PluginCommands;
};
