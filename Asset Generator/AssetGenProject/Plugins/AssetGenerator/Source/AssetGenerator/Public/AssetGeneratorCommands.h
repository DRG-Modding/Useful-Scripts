// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "AssetGeneratorStyle.h"

class FAssetGeneratorCommands : public TCommands<FAssetGeneratorCommands>
{
public:

	FAssetGeneratorCommands()
		: TCommands<FAssetGeneratorCommands>(TEXT("AssetGenerator"), NSLOCTEXT("Contexts", "AssetGenerator", "AssetGenerator Plugin"), NAME_None, FAssetGeneratorStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
