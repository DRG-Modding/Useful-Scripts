#pragma once

#include "CoreMinimal.h"
#include "ParseJSON.h"

class AssetGenOperation
{
private:
	static TArray<FAssetInfo> Objects;
	int ObjectIndex = 0;

	FName GetAssetFName();
	const TCHAR* GetPackageName();
	UBlueprint* CreateBlueprint(UClass* ParentClass, UPackage* Package);
	void CreateAssetPackage();
	
public:
	static void GenerateAssets();
};
