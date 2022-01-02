#include "AssetGenOperation.h"

UClass* AssetGenOperation::GetAssetClass(FString AssetType)
{
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
	UE_LOG(LogTemp, Warning, TEXT("AssetGenOperation: Unknown asset type: %s"), *AssetType);
	return nullptr;
}

UFactory* AssetGenOperation::GetAssetFactory(FString AssetType)
{
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
	} else
	{
		UE_LOG(LogTemp, Error, TEXT("JSON Parse: Failed to deserialise!"));
	}
}

void AssetGenOperation::GenerateAssets(const FString JsonString)
{
	ParseJSON(JsonString);
	
	// Create assets in the Content for each object
	for (int i = 0; i < Objects.Num(); i++)
	{
		FString Path = FPaths::ProjectContentDir() + Objects[i].Path;
		UE_LOG(LogTemp, Warning, TEXT("AssetGenOperation: Asset path: %s"), *Path);
		FString Name = Objects[i].Name;
		UClass* AssetClassType = GetAssetClass(Objects[i].Type);
		UFactory* AssetFactoryType = GetAssetFactory(Objects[i].Type);
		if (AssetClassType != nullptr && AssetFactoryType != nullptr)
		{
			FAssetToolsModule& AssetToolsModule = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools");
			AssetToolsModule.Get().CreateAsset(Name, Path, AssetClassType, AssetFactoryType);
			UE_LOG(LogTemp, Display, TEXT("AssetGenOperation: Created asset: %s"), *Name);
		} else
		{
			UE_LOG(LogTemp, Error, TEXT("AssetGenOperation: Failed to create asset: %s"), *Name);
		}
		
		// FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>(TEXT("AssetRegistry"));
		// IAssetRegistry& AssetRegistry = AssetRegistryModule.Get();
		// FString AssetPath = Path;
		// FString AssetName = Name;
		// FString AssetPackageName = FPackageName::FilenameToLongPackageName(AssetPath);
		// if (!AssetRegistry.GetAssetsByPackageName(AssetPackageName, nullptr, EAssetFlags::DefaultObject, true).Num())
		// {
		// 	FAssetToolsModule& AssetToolsModule = FModuleManager::LoadModuleChecked<FAssetToolsModule>("AssetTools");
		// 	IAssetTools& AssetTools = AssetToolsModule.Get();
		// 	AssetTools.CreateAsset(AssetName, AssetPath, Type);
		// }
	}
}
