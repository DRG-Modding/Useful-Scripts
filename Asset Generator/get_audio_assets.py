import os

# Replace with your path to unpacked files
USER_PATH = r'F:/DRG Modding/DRGPacker/_unpacked/FSD/' 
# Change this to whatever specific folder directory you want to start at
PATH = USER_PATH + r'Content/Audio/SoundControl'
# Replace with your path to where you want the output file to be saved
OUTPUT_PATH = r'F:/Github Projects/Other/DRG Modding Org/Useful-Scripts/Asset Generator/Audio Assets/' 

def output():
    music_libraries = []
    concurrencies = []
    attenuations = []
    reverbs = []
    classes = []
    soundmixes = []
    submixes = []
    for _path, _, files in os.walk(PATH):    
        for asset_file in files:
            if asset_file.endswith('.uasset'):
                print(asset_file)
                if asset_file.startswith('ML_'):
                    music_libraries.append(asset_file.split('.')[0])
                if asset_file.startswith('SoundConcurrency'):
                    concurrencies.append(asset_file.split('.')[0])
                if _path.endswith('\\AttenuationGroups'):
                    attenuations.append(asset_file.split('\\')[-1].split('.')[0])
                if _path.endswith('\\ReverbPresets'):
                    reverbs.append(asset_file.split('\\')[-1].split('.')[0])
                if _path.endswith('\\SoundClasses'):
                    classes.append(asset_file.split('\\')[-1].split('.')[0])
                if _path.endswith('\\SoundMixes'):
                    soundmixes.append(asset_file.split('\\')[-1].split('.')[0])
                if _path.endswith('\\SubMixes'):
                    submixes.append(asset_file.split('\\')[-1].split('.')[0])

    with open(OUTPUT_PATH + 'audio_assets.txt', 'w+') as file:
        for ml in music_libraries:
            file.write(ml + '\n')
        file.write('\n')
    # with open(OUTPUT_PATH + 'concurrencies.txt', 'w+') as file:
        for concurrency in concurrencies:
            file.write(concurrency + '\n')
    # with open(OUTPUT_PATH + 'attenuations.txt', 'w+') as file:
        file.write('\n')
        for attenuation in attenuations:
            file.write(attenuation + '\n')
    # with open(OUTPUT_PATH + 'reverbs.txt', 'w+') as file:
        file.write('\n')
        for reverb in reverbs:
            file.write(reverb + '\n')
    # with open(OUTPUT_PATH + 'classes.txt', 'w+') as file:
        file.write('\n')
        for soundclass in classes:
            file.write(soundclass + '\n')
    # with open(OUTPUT_PATH + 'soundmixes.txt', 'w+') as file:
        file.write('\n')
        for soundmix in soundmixes:
            file.write(soundmix + '\n')
    # with open(OUTPUT_PATH + 'submixes.txt', 'w+') as file:
        file.write('\n')
        for submix in submixes:
            file.write(submix + '\n')

output()