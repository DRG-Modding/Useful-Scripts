import json
import os

aic_files = 'F:\DRG Modding\DRGPacker\JSON\Import assets\AIC'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU36P7-all\Content'

def main():
    # open assetTypes json to get the list of aic files
    with open(json_info) as f:
        asset_types = json.load(f)

    # get the list of aic files
    aic_list = asset_types['/Script/Engine.BlueprintGeneratedClass']

    # loop through the aic files in aic_files and check if they are in the aic_list json
    for aic in aic_list:
        for file in os.listdir(aic_files):
            if file in aic:
                # get the filepath of the aic file
                aic_path = os.path.join(aic_files, file)
                # get the output path of the aic file
                out_aic_path = out_path + aic
                # copy the aic file to the output path
                os.system(f'copy "{aic_path}" "{out_aic_path}"')
                print(f'Copied {aic_path} to {out_aic_path}')

if __name__ == '__main__':
    main()