import json
import os

phys_files = 'F:\DRG Modding\Project Generator\FSDTemplateU37P8-all\Content'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'

def main():
    with open(json_info) as f:
        asset_types = json.load(f)

    assets = []
    for type in asset_types:
        for asset in asset_types[type]:
            asset = asset.split('/')[-1]
            assets.append(asset)

    for root, _, files in os.walk(phys_files):
        for file in files:
            if file not in assets:
                if file.startswith('SK_'):
                    phys_path = os.path.join(root, file)
                    os.remove(phys_path)
                    print(f'Removed {phys_path}')

if __name__ == '__main__':
    main()