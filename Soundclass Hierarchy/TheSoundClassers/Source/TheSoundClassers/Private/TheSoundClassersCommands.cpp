// Copyright Epic Games, Inc. All Rights Reserved.

#include "TheSoundClassersCommands.h"

#define LOCTEXT_NAMESPACE "FTheSoundClassersModule"

void FTheSoundClassersCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "TheSoundClassers", "Execute TheSoundClassers action", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
