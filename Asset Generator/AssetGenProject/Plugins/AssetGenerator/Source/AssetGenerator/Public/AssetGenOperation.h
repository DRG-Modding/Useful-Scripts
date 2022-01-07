#pragma once

#include "CoreMinimal.h"
#include "ParseJSON.h"

class AssetGenOperation
{
private:
	static TArray<FAssetInfo> Objects;
	int ObjectIndex = 0;

	static FName GetAssetFName();
	static const TCHAR* GetPackageName();
	static UBlueprint* CreateBlueprint(UClass* ParentClass, UPackage* Package);
	static void CreateAssetPackage();
	
public:
	static void GenerateAssets(const FString JsonString);
};
