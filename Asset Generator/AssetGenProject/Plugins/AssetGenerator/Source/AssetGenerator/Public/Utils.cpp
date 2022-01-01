#include "Utils.h"

void Utils::OpenMessageDialog(EAppMsgType::Type Buttons, const FString Text)
{
	FMessageDialog::Open(Buttons, FText::FromString(Text));
}

bool Utils::GetSelectedButtonFromDialog(const FString Text, EAppMsgType::Type Buttons, EAppReturnType::Type CheckSelected)
{
	if (FMessageDialog::Open(Buttons, FText::FromString(Text)) == CheckSelected)
	{
		return true;
	}
	return false;
}
