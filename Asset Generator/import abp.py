import json
import os

abp_files = 'F:\DRG Modding\DRGPacker\JSON\ABP'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P6-new\Content'

def main():
    # open assetTypes json to get the list of abp files
    with open(json_info) as f:
        asset_types = json.load(f)

    # get the list of abp files
    abp_list = asset_types['/Script/Engine.AnimBlueprintGeneratedClass']

    # loop through the abp files in abp_files and check if they are in the abp_list json
    for abp in abp_list:
        for file in os.listdir(abp_files):
            if file in abp:
                # get the filepath of the abp file
                abp_path = os.path.join(abp_files, file)
                # get the output path of the abp file
                out_abp_path = out_path + abp
                # copy the abp file to the output path
                os.system(f'copy "{abp_path}" "{out_abp_path}"')
                print(f'Copied {abp_path} to {out_abp_path}')

if __name__ == '__main__':
    main()