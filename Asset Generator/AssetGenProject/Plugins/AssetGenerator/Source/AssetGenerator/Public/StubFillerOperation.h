#pragma once

#include "CoreMinimal.h"
#include "Json.h"

struct FArgInfo
{
	FString Name;
	FString Type;
	bool bIsOut;
	bool bIsReturn;
};

struct FFunctionInfo
{
	FString Name;
	TArray<FArgInfo> Args;
};

struct FPropertyInfo
{
	FString Name;
	FString Type;
};

struct FInfo
{
	FString Name;
	FString Inherits;
	TArray<FFunctionInfo> Events;
	TArray<FFunctionInfo> Functions;
	TArray<FPropertyInfo> Properties;
	TArray<FFunctionInfo> Delegates;
};

enum class EType
{
	Event,
	Function,
	Property,
	Delegate
};

class StubFillerOperation
{
private:
	static void ParseFunction(TArray<TSharedPtr<FJsonValue>> FunctionType, FInfo &Info, const EType InfoType);
	static void ParseJSON(const FString JsonString);

	static TArray<FInfo> Objects;
	
public:
	static void FillStubs(const FString JsonString);
};
