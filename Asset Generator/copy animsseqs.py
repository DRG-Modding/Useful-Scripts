import json
import os

as_files = 'F:\DRG Modding\DRGPacker\JSON\Blender\Anims'
out_path = 'F:\DRG Modding\DRGPacker\JSON\Blender\AnimSeqs\Game'

def main():
    # Scan through as_files and copy all files starting with SK_ with the extension .fbx to out_path
    # Make sure that directory hierarchy is preserved
    for root, _, files in os.walk(as_files):
        for file in files:
            if not file.startswith('SK_') and file.endswith('.fbx') or "SK_Banner01_Anim.fbx" in file or "SK_Spacerig_CounterweightCrank_Anim.fbx" in file or "SK_Facility_CareTaker_Body_Anim.fbx" in file or "SK_Facility_CareTaker_Eye_Anim.fbx" in file or "SK_HoopsGame_Slide_Anim.fbx" in file:
                # Copy file to out_path, making sure that any directories in the path are created
                # if they don't already exist
                out_file = os.path.join(out_path, os.path.relpath(root, as_files), file)
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
                with open(os.path.join(root, file), 'rb') as f:
                    with open(out_file, 'wb') as f2:
                        f2.write(f.read())

if __name__ == '__main__':
    main()
