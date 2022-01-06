#include "ParseJSON.h"

TArray<FAssetInfo> ParseJSON::Objects;

void ParseJSON::ParseFunction(TArray<TSharedPtr<FJsonValue>> FunctionType, FAssetInfo &Info, const EType InfoType)
{
	for (int j = 0; j < FunctionType.Num(); j++)
	{
		const TSharedPtr<FJsonObject> Type = FunctionType[j]->AsObject();
		FFunctionInfo FunctionInfo;
		Type->TryGetStringField(FString(UTF8_TO_TCHAR("name")), FunctionInfo.Name);
		TArray<TSharedPtr<FJsonValue>> Args = Type->GetArrayField(FString(UTF8_TO_TCHAR("args")));
		if (Args.Num() > 0)
		{
			for (int k = 0; k < Args.Num(); k++)
			{
				const TSharedPtr<FJsonObject> Arg = Args[k]->AsObject();
				FArgInfo ArgInfo;
				Arg->TryGetStringField(FString(UTF8_TO_TCHAR("name")), ArgInfo.Name);
				Arg->TryGetStringField(FString(UTF8_TO_TCHAR("type")), ArgInfo.Type);
				Arg->TryGetBoolField(FString(UTF8_TO_TCHAR("is_out")), ArgInfo.bIsOut);
				Arg->TryGetBoolField(FString(UTF8_TO_TCHAR("is_return")), ArgInfo.bIsReturn);
				FunctionInfo.Args.Add(ArgInfo);
			}
			
			if (InfoType == EType::Event) { Info.Events.Add(FunctionInfo); }
			else if (InfoType == EType::Function) { Info.Functions.Add(FunctionInfo); }
			else if (InfoType == EType::Delegate) { Info.Delegates.Add(FunctionInfo); }
		}
	}
}

void ParseJSON::ParseObject(const FString JsonString)
{
	TArray<TSharedPtr<FJsonValue>> Json;
    TSharedRef<TJsonReader<>> JsonReader = TJsonReaderFactory<>::Create(JsonString);
    if (FJsonSerializer::Deserialize<>(JsonReader, Json, FJsonSerializer::EFlags::None)) 
    {
    	for (int i = 0; i < Json.Num(); i++)
    	{
    		FAssetInfo Info;
    		const TSharedPtr<FJsonObject> JsonObject = Json[i]->AsObject();

    		JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("type")), Info.Type);
    		JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("bp_class")), Info.Name);
    		JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("path")), Info.Path);
    		JsonObject->TryGetStringField(FString(UTF8_TO_TCHAR("inherits")), Info.Inherits);

    		TArray<TSharedPtr<FJsonValue>> Events = JsonObject->GetArrayField(FString(UTF8_TO_TCHAR("events")));
	        if (Events.Num() > 0) { ParseFunction(Events, Info, EType::Event); }

    		TArray<TSharedPtr<FJsonValue>> Functions = JsonObject->GetArrayField(FString(UTF8_TO_TCHAR("functions")));
    		if (Functions.Num() > 0) { ParseFunction(Functions, Info, EType::Function); }

    		TArray<TSharedPtr<FJsonValue>> Properties = JsonObject->GetArrayField(FString(UTF8_TO_TCHAR("properties")));
	        if (Properties.Num() > 0)
	        {
	            for (int j = 0; j < Properties.Num(); j++)
	            {
	                const TSharedPtr<FJsonObject> Property = Properties[j]->AsObject();
	                FPropertyInfo PropertyInfo;
	                Property->TryGetStringField(FString(UTF8_TO_TCHAR("name")), PropertyInfo.Name);
	                Property->TryGetStringField(FString(UTF8_TO_TCHAR("type")), PropertyInfo.Type);
	                Info.Properties.Add(PropertyInfo);
	            }    
	        }

			TArray<TSharedPtr<FJsonValue>> Delegates = JsonObject->GetArrayField(FString(UTF8_TO_TCHAR("delegates")));
    		if (Delegates.Num() > 0) { ParseFunction(Delegates, Info, EType::Delegate); }
    		
    		Objects.Add(Info);
    	}
    } else { UE_LOG(LogTemp, Error, TEXT("JSON Parse: Failed to deserialise!")); }
}