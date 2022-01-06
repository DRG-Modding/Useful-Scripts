#pragma once

#include "CoreMinimal.h"

class AssetGenUtils
{
public:
	static UClass* GetAssetClass(const FString AssetType);
	static UFactory* GetAssetFactory(const FString AssetType);
};
