import os, json

SAVE_PATH = "conflicts.json"
enum_conflicts = {'CinematicCamera', 'ImageWriteQueue', 'TimeManagement', 'ChaosSolverEngine', 'ClothingSystemRuntimeCommon', 'ProceduralMeshComponent', 'MovieSceneTracks', 'Niagara', 'SlateCore', 'InputCore', 'MagicLeapAR', 'MRMesh', 'MaterialShaderQualitySettings', 'MeshDescription', 'CoreUObject', 'HeadMountedDisplay', 'GeometryCollectionSimulationCore', 'GooglePAD', 'ClothingSystemRuntimeNv', 'MagicLeapLightEstimation', 'LuminRuntimeSettings', 'GameplayTags', 'VariantManagerContent', 'LiveLinkInterface', 'AIModule', 'ChaosNiagara', 'GeometryCollectionCore', 'DatasmithContent', 'NiagaraShader', 'UdpMessaging', 'Slate', 'MagicLeapHandTracking', 'MagicLeapController', 'MagicLeap', 'GameplayTasks', 'OnlineSubsystemUtils', 'GeometryCollectionEngine', 'MovieScene', 'MagicLeapARPin', 'PhysicsCore', 'MagicLeapEyeTracker', 'MediaAssets', 'EditableMesh', 'InteractiveToolsFramework', 'Foliage', 'EyeTracker', 'EngineSettings', 'UMG', 'ChaosCloth', 'MovieSceneCapture', 'Landscape', 'MagicLeapIdentity', 'Synthesis', 'MediaUtils', 'NavigationSystem', 'MagicLeapPrivileges', 'OnlineSubsystem', 'ImageWrapper', 'VectorVM', 'MagicLeapPlanes'} | \
                 {'AppleImageUtils', 'AugmentedReality', 'AudioPlatformConfiguration', 'ActorSequence', 'AnimationCore', 'AssetTags', 'AudioMixer', 'AnimGraphRuntime'}


def save_conflicts_from_ue_source(ue_source_path):  # e.g. .../UE_4.25/Engine/Source/
    conflicts = set()
    for folder, subs, files in os.walk(ue_source_path):
        for filename in files:
            name = filename.split(".")[0]
            if len(name) > 3:
                conflicts.add(name)
            else:
                #print(name, folder)
                pass
    json.dump(list(conflicts), open(SAVE_PATH, "w"))


def load_conflicts():
    return json.load(open(SAVE_PATH))


def move_conflicts(from_path, to_path):
    print("Excluding UE4 headers...")
    conflicts = load_conflicts()
    os.makedirs(to_path, exist_ok=True)
    c = 0
    for filename in os.listdir(from_path):
        if file_conflicts(conflicts, filename):
            c += 1
            os.rename(os.path.join(from_path, filename),
                      os.path.join(to_path, filename))
    print(f"{c} UE source header conflicts moved to {to_path}")


def file_conflicts(conflicts, filename):
    names = filename.split(".")[0].split("_")
    if names[0] in {"Widget", "ABP", "BP", "UI", "HUD", "ITM", "LCD", "WND"} or "FSD" in filename:
        return False
    for name in names:
        for conflict in conflicts:
            if conflict == name:
                #print(conflict, "in", filename)
                return True
    for conflict in enum_conflicts:
        if conflict in filename:
            return True
    return False


