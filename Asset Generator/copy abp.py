import json
import os

abp_files = 'F:\DRG Modding\Project Generator\FSDTemplateU37P8-all\Content'
json_info = 'F:\DRG Modding\DRGPacker\JSON\AssetTypes.json'
out_path = 'F:\DRG Modding\DRGPacker\JSON\ABPs'

def main():
    with open(json_info) as f:
        asset_types = json.load(f)

    abp_list = asset_types['/Script/Engine.AnimBlueprintGeneratedClass']
    unused_list = abp_list.copy()

    for abp in abp_list:
        full = abp
        abp = abp.split('/')[-1]
        for root, _, files in os.walk(abp_files):
            for file in files:
                if file == abp:
                    out_file = os.path.join(out_path, os.path.relpath(root, abp_files), file)
                    os.makedirs(os.path.dirname(out_file), exist_ok=True)
                    with open(os.path.join(root, file), 'rb') as f:
                        with open(out_file, 'wb') as f2:
                            f2.write(f.read())
                    print(f'Copied {os.path.join(root, file)} to {out_file}')
                    unused_list.remove(full)

    print(f'Unused ABPs: {unused_list}')

if __name__ == '__main__':
    main()