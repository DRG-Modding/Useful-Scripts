### Written by Earthcomputer

import json
import os
import subprocess

drg_parser = r'F:\DRG Modding\DRGParser\DeepRockUnpakConverter.exe'
path = r'F:\DRG Modding\DRGPacker\unpacked\FSD\Content\Audio\SoundControl\SoundClasses'

# def create_json(asset_file):
#     subprocess.run([drg_parser, asset_file], capture_output=True, check=True)

# for asset_file in os.listdir(path):
#     if asset_file.endswith('.uasset'):
#         create_json(os.path.join(path, asset_file))

def print_tree(file, prefix = ''):
    json_file = os.path.join(path, file + '-UAsset.json')
    if not os.path.exists(json_file):
        return
    with open(json_file) as f:
        data = json.load(f)
    export_values = data['ExportValues'][0]
    print(prefix + export_values['Object'])
    potential_props = export_values['Potential Properties']
    for prop in potential_props:
        if prop['Property'] == 'ChildClasses':
            for data_value in prop['Data Value']['Items']:
                if data_value.startswith('Import:'):
                    print_tree(data_value[7:], prefix + ' | ')


print_tree('Master')
