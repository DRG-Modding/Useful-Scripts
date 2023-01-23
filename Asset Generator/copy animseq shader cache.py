import json
import os

as_files = 'C:/Users/Bobby/AppData/Local/UnrealEngine/Common/DerivedDataCache'
out_path = 'F:/DRG Modding/DRGPacker/JSON/Blender/DerivedDataCache'

def main():
    for root, _, files in os.walk(as_files):
        for file in files:
            if file.startswith('ANIMSEQ_'):
                out_file = os.path.join(out_path, os.path.relpath(root, as_files), file)
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
                with open(os.path.join(root, file), 'rb') as f:
                    with open(out_file, 'wb') as f2:
                        f2.write(f.read())
                print(f'{out_file}')

if __name__ == '__main__':
    main()
