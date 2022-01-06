#include "AssetGenUtils.h"
#include "Engine/Blueprint.h"
#include "Blueprint/UserWidget.h"
#include "Engine/DataAsset.h"
#include "WidgetBlueprint.h"
#include "Animation/AnimBlueprint.h"
#include "Factories/SkeletonFactory.h"
#include "Factories/BlueprintFactory.h"
#include "Factories/BlueprintFunctionLibraryFactory.h"
#include "Factories/EnumFactory.h"
#include "Factories/DataAssetFactory.h"
#include "Factories/Factory.h"
#include "Factories/AnimBlueprintFactory.h"
#include "UMGEditor/Classes/WidgetBlueprintFactory.h"
#include "Kismet/BlueprintFunctionLibrary.h"

UClass* AssetGenUtils::GetAssetClass(const FString AssetType)
{
    if (AssetType == "Announcement" || AssetType == "Basic" || AssetType == "HUD" || AssetType == "ITEM" 
    	|| AssetType == "LCD" || AssetType == "MENU" || AssetType == "Options" || AssetType == "Popup" 
    	|| AssetType == "TOOLTIP" || AssetType == "UI" || AssetType == "WeaponDisplay" || AssetType == "Widget" 
    	|| AssetType == "WND")
    {
    	return UWidgetBlueprint::StaticClass();
    }
	if (AssetType == "BP" || AssetType == "ENE" || AssetType == "OBJ" || AssetType == "PRJ" || AssetType == "WPN")
	{
		return UBlueprint::StaticClass();
	}
	if (AssetType == "BPL" || AssetType == "LIB")
	{
		return UBlueprintFunctionLibrary::StaticClass();
	}
	if (AssetType == "WPN")
	{
		return UDataAsset::StaticClass();
	}
	if (AssetType == "ABP")
	{
		return UAnimBlueprint::StaticClass(); 
    }
	if (AssetType == "ENUM")
	{
		return UEnum::StaticClass();
	}
	if (AssetType == "SK")
    {
    	return USkeleton::StaticClass();
    }
	UE_LOG(LogTemp, Warning, TEXT("AssetGenOperation: Unknown asset type: %s"), *AssetType);
	return nullptr;
}

UFactory* AssetGenUtils::GetAssetFactory(const FString AssetType)
{
	if (AssetType == "Announcement" || AssetType == "Basic" || AssetType == "HUD" || AssetType == "ITEM" 
		|| AssetType == "LCD" || AssetType == "MENU" || AssetType == "Options" || AssetType == "Popup" 
		|| AssetType == "TOOLTIP" || AssetType == "UI" || AssetType == "WeaponDisplay" || AssetType == "Widget" 
		|| AssetType == "WND") {
		return NewObject<UWidgetBlueprintFactory>(); 
    }
	if (AssetType == "BP" || AssetType == "ENE" || AssetType == "OBJ" || AssetType == "PRJ" || AssetType == "WPN")
	{
		return NewObject<UBlueprintFactory>();
	}
	if (AssetType == "BPL" || AssetType == "LIB")
	{
		return NewObject<UBlueprintFunctionLibraryFactory>();
	}
	if (AssetType == "WPN")
	{
		return NewObject<UDataAssetFactory>();
	}
	if (AssetType == "ABP")
	{
		return NewObject<UAnimBlueprintFactory>();
    }
	if (AssetType == "ENUM") 
	{
		return NewObject<UEnumFactory>();
	}
	if (AssetType == "SK")
	{
		return NewObject<USkeletonFactory>();
	}
	UE_LOG(LogTemp, Warning, TEXT("AssetGenOperation: Unknown asset type: %s"), *AssetType);
	return nullptr;
}