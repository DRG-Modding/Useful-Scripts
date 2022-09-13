import os
from shutil import copyfile
import json

INPUT_PATH = r'Asset Generator\AssetTypes.json' # Path of asset locations JSON
COOKED_PATH = r'F:/DRG Modding/DRGPacker/_unpacked/FSD/Content' # Path of unpacked files
OUTPUT_PATH = r'F:/DRG Modding/UE4GameProjectGenerator/FSDTemplateU36/Content' # Path of project Content folder

def is_type(asset_type):
    if asset_type == '/Script/Engine.StaticMesh': return True
    elif '/Script/Engine.Anim' in asset_type and not 'Blueprint' in asset_type: return True
    elif asset_type == '/Script/Engine.ParticleSystem': return True
    elif '/Script/Niagara.Niagara' in asset_type: return True
    elif asset_type == '/Script/Engine.SoundClass': return True
    elif asset_type == '/Script/Engine.SoundMix': return True
    elif '/Script/Engine.Submix' in asset_type: return True
    elif asset_type == '/Script/Engine.SoundAttenuation': return True
    elif asset_type == '/Script/Engine.SoundConcurrency': return True
    elif asset_type == '/Script/Engine.ReverbEffect': return True
    else: return False

def main():
    with open(INPUT_PATH, 'r') as file:
        locations = json.load(file)
        for asset_type in locations:
            if is_type(asset_type):
                for asset_path in locations[asset_type]:
                    input_path = COOKED_PATH + asset_path
                    bulk_input_path = input_path[:input_path.rfind('.')] + '.ubulk'
                    output_path = OUTPUT_PATH + asset_path
                    uexp_output_path = output_path[:output_path.rfind('.')] + '.uexp'
                    bulk_output_path = output_path[:output_path.rfind('.')] + '.ubulk'
                    
                    if os.path.exists(input_path):
                        if not os.path.exists(os.path.dirname(output_path)):
                            os.makedirs(os.path.dirname(output_path))
                        copyfile(input_path, output_path)
                        copyfile(input_path, uexp_output_path)
                        if os.path.exists(bulk_input_path): copyfile(input_path, bulk_output_path)
                    else:
                        print(f'{input_path} does not exist')

if __name__ == '__main__':
    main()