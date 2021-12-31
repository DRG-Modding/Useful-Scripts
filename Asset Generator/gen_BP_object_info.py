import json
import os
import re

PATH = r'C:/../../../../Github Projects/Header-Dumps/U35.63118/DUMP/' # Replace with your path to dumped files
OUTPUT_PATH = r'C:/../../../../Github Projects/Useful-Scripts/Asset Generator/' # Replace with your path to where you want the output file to be saved

def check_startswith(string):
    WHITELIST_START = ['BP_', 'ENE_', 'BPL_', 'OBJ_', 'LIB_', 'PRJ_', 'WPN_']
    for start in WHITELIST_START:
        if string.startswith(start): return True
    return False

def check_contains(string, type):
    BLACKLIST_PROPERTIES = ['ubergraph', 'onloaded_', 'defaultsceneroot']
    BLACKLIST_FUNCTIONS = ['ubergraph', 'onloaded_', 'receivebeginplay', 'receivedestroyed', 'receivetick', 'userconstructionscript', 'ontick_']
    if type == 'property':
        for property in BLACKLIST_PROPERTIES:
            if property in string.lower(): return True
        return False
    elif type == 'function':
        for function in BLACKLIST_FUNCTIONS:
            if function in string.lower(): return True
        return False

def match_variables(line, properties, type):
    match = re.search(type + r'\s(.*);\s\/\/(.*)+', line)
    if match:
        # If variable is an uber, ignore
        name = match.group(1)
        if not check_contains(name, 'property'):
            # If type is 'enum' then it is an enum class type
            if 'enum' in type:
                names = name.split(' ')
                name = names[-1]
                type = type + ' ' + ' '.join(names[:-1])
            type = type.replace('*', '')
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
        if not check_contains(name, 'function'):
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
                        arg_type = arg_type.replace('*', '')
                        function_properties.append({
                            'name': arg_name,
                            'type': arg_type
                        })
            type = type.replace('*', '')
            functions.append({
                'name': name,
                'type': type,
                'args': function_properties
            })
    return functions

def output():
    output = []
    for asset_file in os.listdir(PATH):
        if asset_file.endswith('.h'):
            if check_startswith(asset_file):
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
                    type = type.replace('*', '')

                    # Match variables
                    properties = match_variables(line, properties, type)

                    # Match functions
                    functions = match_functions(line, functions, type)
                output.append({
                    'bp_name': name,
                    'inherits': inherits,
                    'functions': functions,
                    'properties': properties
                })

    with open(OUTPUT_PATH + 'BP_object_info.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()