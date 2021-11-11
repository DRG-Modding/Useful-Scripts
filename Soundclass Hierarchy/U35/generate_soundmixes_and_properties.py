import json
import os

path = r'F:\DRG Modding\DRGPacker\U35.63118\FSD\Content\Audio\SoundControl\SoundMixes'

def print_soundmixes():
    output = []
    for asset_file in os.listdir(path):
        # Construct json file
        json_file = os.path.join(path, asset_file)
        if not os.path.exists(json_file) or not json_file.endswith('.json'):
            pass
        else:
            # Load json file
            with open(json_file) as f:
                data = json.load(f)

                # Get soundclass parents
                prefix_path = '/Game/Audio/SoundControl/SoundClasses/'
                soundclass_names = []
                imports = data['importMap']['imports']
                for import_ in imports:
                    name = import_['name']
                    if name.startswith(prefix_path):
                        soundclass_names.append(name.replace(prefix_path, ''))
                        soundclass_names[-1] = soundclass_names[-1][:-4]

                # Get soundmix name
                exports_expansion = data['exportsExpansion']
                soundmix_name = exports_expansion[0]['name']

                # Get soundmix properties
                properties = exports_expansion[0]['properties']
                data_values = {
                    'InitialDelay': 0.0,
                    'FadeInTime': 0.00,
                    'FadeOutTime': 0.0,
                    'Duration': -1,
                    'bApplyEQ': False,
                }
                for prop in properties:
                    if prop['name'] in ['InitialDelay', 'FadeInTime', 'FadeOutTime', 'Duration', 'bApplyEQ']:
                        data_values[prop['name']] = prop['contents'][0]['value']
                    elif prop['name'] in ['SoundClassEffects', 'EQSettings']:
                        continue
                    else:
                        data_values[prop['name']] = 0

                output.append({
                    'soundmix_name' : soundmix_name,
                    'data_values' : data_values,
                    'soundclass_names' : soundclass_names
                })

    # Write json file
    with open('F:/Github Projects/Other/DRG Modding Org/Useful-Scripts/Soundclass Hierarchy/U35/soundmixes.json', 'w+') as file:
        json.dump(output, file, indent=2)

print_soundmixes()