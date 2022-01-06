#include "AssetGenOperation.h"

TArray<FInfo> AssetGenOperation::Objects;

UClass* AssetGenOperation::GetAssetClass(FString AssetType)
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

UFactory* AssetGenOperation::GetAssetFactory(FString AssetType)
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
		return nullptr;
		// return NewObject<UBlueprintFunctionLibraryFactory>();
	}
	if (AssetType == "WPN")
	{
		return NewObject<UDataAssetFactory>();
	}
	if (AssetType == "ABP")
	{
		return nullptr;
        // return NewObject<UAnimBlueprintFactory>();
    }
	if (AssetType == "ENUM") 
	{
		return nullptr;
		// return NewObject<UEnumFactory>();
	}
	if (AssetType == "SK")
	{
		// return NewObject<USkeletonFactory>();
		return nullptr;
	}
	UE_LOG(LogTemp, Warning, TEXT("AssetGenOperation: Unknown asset type: %s"), *AssetType);
	return nullptr;
}

void AssetGenOperation::ParseJSON(const FString JsonString)
{
	TArray<TSharedPtr<FJsonValue>> Json;
	TSharedRef<TJsonReader<>> JsonReader = TJsonReaderFactory<>::Create(JsonString);
	if (FJsonSerializer::Deserialize<>(JsonReader, Json, FJsonSerializer::EFlags::None)) 
	{
		for (int i = 0; i < Json.Num(); i++)
		{
			FInfo Info;
			const TSharedPtr<FJsonObject> JsonObject = Json[i]->AsObject();
			JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("type")), Info.Type);
			JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("name")), Info.Name);
			JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("path")), Info.Path);
			Objects.Add(Info);
		}
	} else { UE_LOG(LogTemp, Error, TEXT("JSON Parse: Failed to deserialise!")); }
}

void AssetGenOperation::GenerateAssets(const FString JsonString)
{
	ParseJSON(JsonString);
	
	// Create assets in the Content for each object
	for (int i = 0; i < Objects.Num(); i++)
	{
		FString Path = FString(UTF8_TO_TCHAR("/")) + Objects[i].Path;
		UE_LOG(LogTemp, Display, TEXT("AssetGenOperation: Asset path: %s"), *Path);
		FString Name = Objects[i].Name;
		UClass* AssetClassType = GetAssetClass(Objects[i].Type);
		UFactory* AssetFactoryType = GetAssetFactory(Objects[i].Type);
		if (AssetClassType != nullptr && AssetFactoryType != nullptr)
		{
			FAssetToolsModule& AssetToolsModule = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools");
			UObject* NewAsset = AssetToolsModule.Get().CreateAsset(Name, Path, AssetClassType, AssetFactoryType);
			UE_LOG(LogTemp, Display, TEXT("AssetGenOperation: Created asset: %s"), *Name);

			// Save the asset
			if (NewAsset != nullptr)
			{
				UPackage* Package = NewAsset->GetOutermost();
				Package->MarkPackageDirty();
				FString PackageFileName = FPackageName::LongPackageNameToFilename(Package->GetName(), FPackageName::GetAssetPackageExtension());
				FString PackageFilePath = FPaths::ConvertRelativePathToFull(FPaths::ProjectContentDir() + Path);
				FString PackageFile = PackageFilePath + "/" + PackageFileName;
				if (FPackageName::DoesPackageExist(Package->GetName()))
				{
					UPackage::SavePackage(Package, nullptr, RF_Standalone, *PackageFile);
					UE_LOG(LogTemp, Display, TEXT("AssetGenOperation: Saved package: %s"), *PackageFile);
				}
			}
		} else { UE_LOG(LogTemp, Error, TEXT("AssetGenOperation: Failed to create asset: %s"), *Name); }
	}
}
