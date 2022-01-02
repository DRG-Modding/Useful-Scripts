#pragma once

#include "CoreMinimal.h"
#include "Misc/MessageDialog.h"

class Utils
{
public:
	static void OpenMessageDialog(EAppMsgType::Type Buttons, const FString Text)
	{
		FMessageDialog::Open(Buttons, FText::FromString(Text));
	}
	
	static bool GetSelectedButtonFromDialog(const FString Text, EAppMsgType::Type Buttons, EAppReturnType::Type CheckSelected)
	{
		if (FMessageDialog::Open(Buttons, FText::FromString(Text)) == CheckSelected)
		{
			return true;
		}
		return false;
	}
};
