import json
import os
import re

PATH = r'C:/../../../../Github Projects/Header-Dumps/U35.63118/DUMP/' # Replace with your path to dumped files
OUTPUT_PATH = r'C:/../../../../Github Projects/Useful-Scripts/Asset Generator/' # Replace with your path to where you want the output file to be saved

def match_variables(line, properties, type):
    match = re.search(type + r'\s(.*);\s\/\/(.*)+', line)
    if match:
        # If variable is an uber, ignore
        name = match.group(1)
        lname = name.lower()
        if not ('ubergraph' in lname or 'OnLoaded_' in name):
            # Remove the '\\' from before the '*' if it exists
            type = type.replace('\\', '')
            properties.append({
                'name': name,
                'type': type
            })
            pass
    return properties

def match_functions(line, functions, type):
    match = re.search(type + r'\s(\w+)\((.*)\);', line)
    if match:
        # If function is a recieve, bind or ubergraph, ignore
        name = match.group(1)
        lname = name.lower()
        if not ('recieve' in lname or 'ubergraph' in lname\
        or 'OnLoaded_' in name or 'receive' in lname):
            # Add the args of the function
            args = match.group(2).split(', ')
            if args is not None:
                function_properties = []
                for arg in args:
                    arg = arg.strip()
                    try:
                        if 'enum' in arg: # We do a little cheeky hardcoding
                            # Type is all the elements except the last one 
                            arg_type = ' '.join(arg.split(' ')[:-1])
                            arg_name = arg.split(' ')[-1]
                        else:
                            # Name is all the elements except the first one
                            arg_type = arg.split(' ')[0]
                            arg_name = ' '.join(arg.split(' ')[1:])
                    except IndexError:
                        arg_type, arg_name = arg, ''
                    if arg != '':
                        function_properties.append({
                            'name': arg_name,
                            'type': arg_type
                        })
            function_properties = check_len(function_properties)
            functions.append({
                'name': name,
                'args': function_properties
            })
    return functions

def check_len(array):
    if len(array) == 0: return None
    return array

def output():
    output = []
    for asset_file in os.listdir(PATH):
        if asset_file.endswith('.h'):
            if asset_file.startswith('BP_') or asset_file.startswith('ENE_')\
            or asset_file.startswith('BPL_') or asset_file.startswith('OBJ_')\
            or asset_file.startswith('LIB_') or asset_file.startswith('PRJ_')\
            or asset_file.startswith('WPN_'):
                # Open asset file
                with open(PATH + asset_file) as f:
                    data = f.read()
                lines = data.split('\n')

                name = asset_file.split('_classes.h')[0]
                inherits = lines[2].split(' : ')[1].strip(' {')[1:]
                properties = []
                functions = []

                # Remove the first 3 elements of lines
                lines = lines[3:]
                for line in lines:
                    if line == '' or line == '};': continue
                    line = line.replace('\t', '')
                    
                    type = line.split(' ')[0]
                    # Check for pointer which fucks up the regex
                    if type[-1] == '*': type = type.replace('*', '\*')

                    # Match variables
                    properties = match_variables(line, properties, type)

                    # Match functions
                    functions = match_functions(line, functions, type)

                properties = check_len(properties)
                functions = check_len(functions)
                output.append({
                    'bp_name': name,
                    'inherits': inherits,
                    'properties': properties,
                    'functions': functions
                })

    with open(OUTPUT_PATH + 'BP_object_info.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()