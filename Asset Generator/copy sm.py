import json
import os

sm_files = 'F:\DRG Modding\Project Generator\FSDTemplateU37P8-all\Content'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\Project Generator\FSDTemplateU37P8-all\Content'

def main():
    with open(json_info) as f:
        asset_types = json.load(f)

    sm_list = asset_types['/Script/Engine.StaticMesh']

    for sm in sm_list:
        sm = sm.split('/')[-1]
        for root, _, files in os.walk(sm_files):
            for file in files:
                if file == sm:
                    out_file = os.path.join(out_path, os.path.relpath(root, sm_files), file)
                    os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    with open(os.path.join(root, file), 'rb') as f:
                        with open(out_file, 'wb') as f2:
                            f2.write(f.read())
                    print(f'Copied {os.path.join(root, file)} to {out_file}')

if __name__ == '__main__':
    main()