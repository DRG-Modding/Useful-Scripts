import json
import os

json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
in_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P6-new\Content'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P7-all\Content'

def main():
    # open assetTypes json to get the list of id files
    with open(json_info) as f:
        asset_types = json.load(f)

    # get the list of id files
    id_list = asset_types['/Script/FSD.ItemID']

    # loop through the id files in id_files and check if they are in the id_list json
    for id in id_list:
        for root, _, files in os.walk(in_path):
            for file in files:
                actual = root.replace(in_path, '').replace('\\', '/') + '/' + file 
                if 'Audio' in actual: continue
                if actual == id:
                    # get the output path of the id file
                    out_id_path = out_path + id
                    # copy the id file to the output path
                    os.system(f'copy "{root}" "{out_id_path}"')
                    print(f'Copied {root} to {out_id_path}')

if __name__ == '__main__':
    main()