import os

REF_FILEPATH = r'F:\DRG Modding\DRGPacker\unpacked\FSD\Content\Audio\Music\JukeBox'
DEST_FILEPATH = r'F:\DRG Modding\MODS\Coffee Stain Games Jukebox Music Pak\Content - Copy\Audio\Music\JukeBox'

def rename_jukebox_music(dest_dir, ref_dir):
    for root, _, files in os.walk(dest_dir):
        relpath = os.path.relpath(root, dest_dir)
        from_root = os.path.join(ref_dir, relpath)
        FROM_SUFFIX = '.uasset'
        from_files = [f[:-len(FROM_SUFFIX)] for f in os.listdir(from_root) if f.endswith(FROM_SUFFIX)]
        num_to_rename = len(files)
        num_to_choose_from = len(from_files)
        if num_to_choose_from < num_to_rename:
            print('More files in input {} ({}) than there are names to choose from {}'.format(relpath, num_to_rename, num_to_choose_from))
            num_to_rename = num_to_choose_from
        else:
            print('Renaming {} files in {}, choosing from {} possible names'.format(num_to_rename, relpath, num_to_choose_from))
        
        for i, fromfile in enumerate(files):
            if i >= num_to_rename:
                break
            _, extension = os.path.splitext(fromfile)
            newname = from_files[i]
            if len(extension) > 0:
                newname = newname + '.' + extension
            os.rename(os.path.join(root, fromfile), os.path.join(root, newname))

if __name__ == '__main__':
    rename_jukebox_music(DEST_FILEPATH, REF_FILEPATH)