// Copyright Epic Games, Inc. All Rights Reserved.

#include "AssetGeneratorCommands.h"

#define LOCTEXT_NAMESPACE "FAssetGeneratorModule"

void FAssetGeneratorCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "AssetGenerator", "Execute AssetGenerator action", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
