#include "AssetGenOperation.h"
#include "AssetGenUtils.h"
#include "AssetRegistryModule.h"
#include "AssetToolsModule.h"
#include "Misc/Paths.h"
#include "Blueprint/UserWidget.h"
#include "K2Node_FunctionEntry.h"
#include "Dom/JsonObject.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "BlueprintCompilationManager.h"
#include "EdGraphSchema_K2_Actions.h"
#include "K2Node_CallParentFunction.h"
#include "K2Node_CustomEvent.h"
#include "K2Node_Event.h"
#include "K2Node_FunctionResult.h"
#include "Engine/SimpleConstructionScript.h"
#include "Kismet2/KismetEditorUtilities.h"

FName AssetGenOperation::GetAssetFName()
{
	return FName(Objects[ObjectIndex].Name);
}

const TCHAR* AssetGenOperation::GetPackageName()
{
	return *Objects[ObjectIndex].Path;
}

UBlueprint* AssetGenOperation::CreateBlueprint(UClass* ParentClass, UPackage* Package)
{
	EBlueprintType BlueprintType = BPTYPE_Normal;
	if (ParentClass->HasAnyClassFlags(CLASS_Const)) { BlueprintType = BPTYPE_Const; }
	if (ParentClass == UBlueprintFunctionLibrary::StaticClass())
	{ BlueprintType = BPTYPE_FunctionLibrary; }
	if (ParentClass == UInterface::StaticClass())
	{ BlueprintType = BPTYPE_Interface; }
	return FKismetEditorUtilities::CreateBlueprint(ParentClass, Package, GetAssetFName(), BlueprintType, 
	UBlueprint::StaticClass(), UBlueprintGeneratedClass::StaticClass());
}

void AssetGenOperation::CreateAssetPackage() {
	// const int32 SuperStructIndex = GetAssetData()->GetIntegerField(TEXT("SuperStruct"));
	// UClass* ParentClass = Cast<UClass>(GetObjectSerializer()->DeserializeObject(SuperStructIndex));
	//
	// if (ParentClass == NULL) {
	// 	UE_LOG(LogTemp, Error, TEXT("AssetGenOperation: Cannot resolve parent class %s for blueprint %s"), *ParentClass, *GetAssetFName().ToString());
	// 	ParentClass = GetFallbackParentClass();
	// }
	//
	// UPackage* NewPackage = CreatePackage(*GetPackageName());
	// UBlueprint* NewBlueprint = CreateNewBlueprint(NewPackage, ParentClass);
	// SetPackageAndAsset(NewPackage, NewBlueprint, false);
	//
	// UpdateDeserializerBlueprintClassObject(true);
	// MarkAssetChanged();
}

void AssetGenOperation::GenerateAssets()
{
	// Create assets in the Content for each object
	for (int i = 0; i < Objects.Num(); i++)
	{
		FString Path = FString(UTF8_TO_TCHAR("/")) + Objects[i].Path;
		UE_LOG(LogTemp, Display, TEXT("AssetGenOperation: Asset path: %s"), *Path);
		FString Name = Objects[i].Name;
		UClass* AssetClassType = AssetGenUtils::GetAssetClass(Objects[i].Type);
		UFactory* AssetFactoryType = AssetGenUtils::GetAssetFactory(Objects[i].Type);
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
