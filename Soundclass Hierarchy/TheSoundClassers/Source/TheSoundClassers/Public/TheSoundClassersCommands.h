// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "TheSoundClassersStyle.h"

class FTheSoundClassersCommands : public TCommands<FTheSoundClassersCommands>
{
public:

	FTheSoundClassersCommands()
		: TCommands<FTheSoundClassersCommands>(TEXT("TheSoundClassers"), NSLOCTEXT("Contexts", "TheSoundClassers", "TheSoundClassers Plugin"), NAME_None, FTheSoundClassersStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
