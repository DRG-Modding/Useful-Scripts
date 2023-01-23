import json
import os

id_files = 'F:\DRG Modding\DRGPacker\JSON\Import assets\ID'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P7-all\Content'

def main():
    # open assetTypes json to get the list of id files
    with open(json_info) as f:
        asset_types = json.load(f)

    # get the list of id files
    id_list = asset_types['/Script/FSD.ItemID']

    # loop through the id files in id_files and check if they are in the id_list json
    for id in id_list:
        for file in os.listdir(id_files):
            if file in id:
                # get the filepath of the id file
                id_path = os.path.join(id_files, file)
                # get the output path of the id file
                out_id_path = out_path + id
                # copy the id file to the output path
                os.system(f'copy "{id_path}" "{out_id_path}"')
                print(f'Copied {id_path} to {out_id_path}')

if __name__ == '__main__':
    main()