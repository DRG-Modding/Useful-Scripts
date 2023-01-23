import json
import os

esi_files = 'F:\DRG Modding\DRGPacker\JSON\Import assets\ESI'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P7-all\Content'

def main():
    # open assetTypes json to get the list of esi files
    with open(json_info) as f:
        asset_types = json.load(f)

    # get the list of esi files
    esi_list = asset_types['/Script/Engine.BlueprintGeneratedClass']

    # loop through the esi files in esi_files and check if they are in the esi_list json
    for esi in esi_list:
        for file in os.listdir(esi_files):
            if file in esi:
                # get the filepath of the esi file
                esi_path = os.path.join(esi_files, file)
                # get the output path of the esi file
                out_esi_path = out_path + esi
                # copy the esi file to the output path
                os.system(f'copy "{esi_path}" "{out_esi_path}"')
                print(f'Copied {esi_path} to {out_esi_path}')
                
if __name__ == '__main__':
    main()