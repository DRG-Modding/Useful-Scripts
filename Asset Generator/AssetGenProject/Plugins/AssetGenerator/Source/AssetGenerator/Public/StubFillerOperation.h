#pragma once

#include "CoreMinimal.h"
#include "Json.h"
#include "ParseJSON.h"

class StubFillerOperation
{
private:
	static TArray<FAssetInfo> Objects;
	
public:
	static void FillStubs();
};
