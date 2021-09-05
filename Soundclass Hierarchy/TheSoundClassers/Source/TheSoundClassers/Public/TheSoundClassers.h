// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"
#include "Sound/SoundClass.h"
#include "PackageHelperFunctions.h"

class FToolBarBuilder;
class FMenuBuilder;


#define LOCTEXT_NAMESPACE "FTheSoundClassersModule"

class MyNodeClass {
public:
	FString name;
	TArray<TSharedPtr<MyNodeClass>> MyNodeChildren = TArray<TSharedPtr<MyNodeClass>>();
	UINT16 Depth;

	USoundClass* theLoadedFile;

	MyNodeClass(FString InName, int theDepth) {
		name = InName;
		Depth = theDepth;

		FString Path = "/Game/SoundClasses/" + name;
		theLoadedFile = LoadObject<USoundClass>(nullptr, *Path);
		if (theLoadedFile == nullptr) {
			UE_LOG(LogTemp, Error, TEXT("Failed to load %s"), *name);
		}
		UE_LOG(LogTemp, Error, TEXT("Failed to load %s"), *name);
	}

	void ParseConfig(TArray<FString> * ConfigFile, int currentLine) {
		if (Depth > 100) {
			return;
		}
		int currentLoopFile = currentLine + 1;
		while (true) {
			int theFuckingMax = (*ConfigFile).Num();
			if (currentLoopFile >= theFuckingMax) { //End of file
				break;
			}
			FString theLine = (*ConfigFile)[currentLoopFile];
			volatile int theStringDepth = CountVerticalLines(theLine);
			if (theStringDepth == Depth + 1) { // If the next index is a child, or one depth below us.
				TSharedPtr<MyNodeClass> theNewNode = MakeShared<MyNodeClass>(ParseName(theLine, Depth + 1), Depth + 1);
				theNewNode->ParseConfig(ConfigFile, currentLoopFile);
				MyNodeChildren.Add(theNewNode);
			}
			else if (theStringDepth == Depth) { // If the next index is on the same depth as us.
				break;
			}
			currentLoopFile++;
		}
	}

	int CountVerticalLines(FString TheLine) {
		int theLength = TheLine.Len();
		int theDepth = 0;
		for (int i = 0; i < theLength; i++) {
			if (TheLine[i] == '|') {
				theDepth++;
			}
			else
			{
				break;
			}
		}
		return theDepth;
	}

	FString ParseName(FString theLine, int toRemove) {
		FString newString = theLine.Right(theLine.Len() - toRemove);
		return newString;
	}

	void ConstructChildren() {
		if (MyNodeChildren.Num() == 0) {
			return;
		}

		theLoadedFile->ChildClasses = TArray<USoundClass*>();

		for (TSharedPtr Child : MyNodeChildren) {
			theLoadedFile->ChildClasses.Add(Child->theLoadedFile);
			Child->ConstructChildren();
		}

		theLoadedFile->MarkPackageDirty();
	}
};

class FTheSoundClassersModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
	
	/** This function will be bound to Command. */
	void PluginButtonClicked();
	
private:

	void RegisterMenus();
	TSharedPtr<MyNodeClass> ConfigParser(FString FileLocation);


private:
	TSharedPtr<class FUICommandList> PluginCommands;
};
