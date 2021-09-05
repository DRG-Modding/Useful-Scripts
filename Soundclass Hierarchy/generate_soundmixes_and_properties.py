import json
import os
import subprocess

drg_parser = r'F:\DRG Modding\DRGParser\DeepRockUnpakConverter.exe'
path = r'F:\DRG Modding\DRGPacker\unpacked\FSD\Content\Audio\SoundControl\SoundMixes'

def create_json(asset_file):
    subprocess.run([drg_parser, asset_file], capture_output=True, check=True)
    print('Created file:' + asset_file)


def print_soundmixes():
    output = []
    for asset_file in os.listdir(path):
        if asset_file.endswith('.uasset'):
            # create_json(os.path.join(path, asset_file))

            json_file = os.path.join(path, asset_file.replace('.uasset', '') + '-UAsset.json')
            if not os.path.exists(json_file):
                pass
            with open(json_file) as f:
                data = json.load(f)

                prefix_path = '/Game/Audio/SoundControl/SoundClasses/'
                soundclass_names = []
                object_imports = data['ObjectImports']
                for objects in object_imports:
                    object_name = objects['ObjectName']
                    if object_name.startswith(prefix_path):
                        soundclass_names.append(object_name.replace(prefix_path, ''))
                        print("objects stuff " + object_name)

                export_values = data['ExportValues'][0]
                soundmix_name = export_values['Object']
                potential_props = export_values['Potential Properties']
                data_values = []
                for prop in potential_props:
                    if prop['Property'] in ['InitialDelay', 'FadeInTime', 'FadeOutTime', 'Duration', 'bApplyEQ', 'EQSettings', 'SoundClassEffects']:
                        data_values.append(prop['Data Value'])
                    else:
                        data_values.append(0)

                output.append({
                    'soundmix_name' : soundmix_name,
                    'data_values' : data_values,
                    'soundclass_names' : soundclass_names
                })
                
    with open('F:\DRG Modding\Scripts\soundmixes.json', 'w+') as file:
        json.dump(output, file, indent=2)


print_soundmixes()
