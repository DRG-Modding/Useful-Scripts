import json

LOCATIONS_PATH = r'C:/Users/../OneDrive/Documents/Github Projects/Useful-Scripts/Asset Generator/BP_names_and_locations.json'
OBJECT_INFO_PATH = r'C:/Users/../OneDrive/Documents/Github Projects/Useful-Scripts/Asset Generator/BP_object_info_ue4ss.json'
OUTPUT_PATH = r'C:/Users/../OneDrive/Documents/Github Projects/Useful-Scripts/Asset Generator/' # Replace with your path to where you want the output file to be saved

def output():
    with open(LOCATIONS_PATH, 'r') as file:
        locations = json.load(file)
    with open(OBJECT_INFO_PATH, 'r') as file:
        object_info = json.load(file)
    output = []
    
    for asset in locations:
        for object in object_info:
            if asset['name'] == object['bp_class']:
                output.append({
                    'type': asset['type'],
                    'bp_class' : asset['name'],
                    'path' : asset['path']
                })
                for key in object:
                    if key == 'bp_class': continue
                    output[-1][key] = object[key]

    with open(OUTPUT_PATH + 'BP_names_and_locations_with_object_info.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()