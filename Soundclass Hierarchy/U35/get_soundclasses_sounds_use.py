import json
import os

# Replace with your path to unpacked files
USER_PATH = r'C:/../../../../DRG Modding/DRGPacker/FSD-WindowsNoEditor/FSD/' 
# Change this to whatever specific folder directory you want to start at
PATH = USER_PATH + r'Content/Audio/WeaponsNTools'
# Replace with your path to where you want the output file to be saved
OUTPUT_PATH = r'C:/../../../../Github Projects/Useful-Scripts/Soundclass Hierarchy/U35/' 

def output():
    output = []
    for _path, _, files in os.walk(PATH):    
        for asset_file in files:
            # Construct json file
            json_file = os.path.join(_path, asset_file)
            if not os.path.exists(json_file) or not json_file.endswith('.json'):
                pass
            else:
                # Load json file
                with open(json_file) as f:
                    data = json.load(f)

                    # Get soundclass
                    soundclass_name = ""
                    imports = data['importMap']['imports']
                    found = False
                    for import_ in imports:
                        if import_['_class'] == 'SoundClass : 0':
                            soundclass_name = import_['name']
                            soundclass_name = soundclass_name.replace(' : 0', '')
                            found = True
                            break
                    if not found:
                        break

                    # Get file name
                    file_name = asset_file.split('.')[0]

                    output.append({
                        'weapon' : file_name,
                        'soundclass' : soundclass_name
                    })

    # Write json file
    with open(OUTPUT_PATH + 'weapon_soundclasses.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()