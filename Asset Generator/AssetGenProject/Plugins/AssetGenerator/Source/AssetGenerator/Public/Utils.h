#pragma once

#include "CoreMinimal.h"
#include "Misc/MessageDialog.h"

class Utils
{
public:
	static void OpenMessageDialog(EAppMsgType::Type Buttons, const FString Text);
	static auto GetSelectedButtonFromDialog(const FString Text, EAppMsgType::Type Buttons, EAppReturnType::Type CheckSelected) -> bool;
};
