import json
import os

USER_PATH = r'C:/../../../../DRG Modding/DRGPacker/FSD-WindowsNoEditor/FSD/' # Replace with your path to unpacked files
PATH = USER_PATH + r'Content'
OUTPUT_PATH = r'C:/../../../../Github Projects/Useful-Scripts/Asset Generator/' # Replace with your path to where you want the output file to be saved

def output():
    output = []
    for _path, _, files in os.walk(PATH):    
        for asset_file in files:
            if asset_file.endswith('.uasset'):
                if asset_file.startswith('BP_') or asset_file.startswith('ENE_')\
                or asset_file.startswith('BPL_') or asset_file.startswith('OBJ_')\
                or asset_file.startswith('LIB_') or asset_file.startswith('PRJ_')\
                or asset_file.startswith('WPN_'):
                    RELATIVE_PATH = _path.replace(USER_PATH, '')
                    output.append({
                        'type': asset_file.split('_')[0],
                        'name' : asset_file.split('.')[0],
                        # 'path' : os.path.join(RELATIVE_PATH, asset_file).replace('\\', '/').split('_')[0].replace(asset_file.split('_')[0], '')
                        'path' : os.path.join(RELATIVE_PATH, asset_file).split('_')[0].replace(asset_file.split('_')[0], '')
                    })
    with open(OUTPUT_PATH + 'BP_names_and_locations.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()