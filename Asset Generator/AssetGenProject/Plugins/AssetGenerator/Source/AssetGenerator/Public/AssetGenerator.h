// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
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

	TArray<FString> AssetNames;
	TArray<FString> AssetLocations;

private:
	void RegisterMenus();

	TSharedPtr<class FUICommandList> PluginCommands;
	FString DialogName = "Open";
	FString DefaultPath = "C:";
	FString DefaultFile = "";
	FString FileTypes = ".json";
	uint32 Flags = 0;
};
