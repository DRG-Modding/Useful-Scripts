#pragma once

#include "CoreMinimal.h"
#include "Json.h"
#include "AssetTypeCategories.h"
#include "AssetRegistryModule.h"
#include "AssetToolsModule.h"
#include "Misc/Paths.h"
#include "Engine/Blueprint.h"
#include "Blueprint/UserWidget.h"
#include "Engine/DataAsset.h"
#include "Factories/BlueprintFactory.h"
#include "Factories/BlueprintFunctionLibraryFactory.h"
#include "Factories/DataAssetFactory.h"
#include "Factories/Factory.h"
#include "Factories/AnimBlueprintFactory.h"
#include "UMGEditor/Classes/WidgetBlueprintFactory.h"
#include "Kismet/BlueprintFunctionLibrary.h"

struct FInfo
{
	FString Type;
	FString Name;
	FString Path;
};

class AssetGenOperation
{
private:
	static UClass* GetAssetClass(FString AssetType);
	static UFactory* GetAssetFactory(FString AssetType);
	static void ParseJSON(const FString JsonString);
	
	static TArray<FInfo> Objects;
	
public:
	static void GenerateAssets(const FString JsonString);
};
