import json
import os

path = r'F:\DRG Modding\DRGPacker\U35.63118\FSD\Content\Audio\SoundControl\SoundClasses'

def print_tree(file, prefix = ''):
    # Construct json file
    json_file = os.path.join(path, file + '.json')
    if not os.path.exists(json_file):
        return
    
    # Open json file
    with open(json_file) as f:
        data = json.load(f)

    # Parse JSON
    exports_expansion = data['exportsExpansion']
    print(prefix + exports_expansion[0]['name'])
    property_types = exports_expansion[0]['properties']
    for prop in property_types:
        if prop['name'] == 'ChildClasses':
            contents = prop['contents']
            i = 0
            for child in contents:
                if i > 1:
                    child_contents = child['contents'][0]['value']
                    if child_contents.startswith('Import:'):
                        print_tree(child_contents[7:], prefix + ' | ')
                i += 1

print_tree('Master')