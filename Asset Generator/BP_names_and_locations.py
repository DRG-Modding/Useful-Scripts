import json
import os

USER_PATH = r'C:/Users/../OneDrive/Documents/DRG Modding/DRGPacker/FSD-WindowsNoEditor/FSD/' # Replace with your path to unpacked files
PATH = USER_PATH + r'Content'
OUTPUT_PATH = r'C:/Users/../OneDrive/Documents/Github Projects/Useful-Scripts/Asset Generator/' # Replace with your path to where you want the output file to be saved

def check_starts_with(string):
    WHITELIST_START = ['ABP_', 'Announcement_', 'Basic_', 'HUD_', 'ITEM_', 'LCD_', 'Lore_', 'MENU_', 'Options_', 'Popup_', 'TOOLTIP_', 'UI_', 'WeaponDisplay_', 'Widget_', 'WND_', 'BP_', 'ENE_', 'BPL_', 'OBJ_', 'LIB_', 'PRJ_', 'WPN_', 'ENUM_', 'SK_']
    WHITELIST_START_CURRENT = ['BP_', 'ENE_', 'BPL_', 'OBJ_', 'LIB_', 'PRJ_', 'WPN_']
    for start in WHITELIST_START_CURRENT:
        if string.startswith(start): return True
    return False

def output():
    output = []
    for _path, _, files in os.walk(PATH):    
        for asset_file in files:
            if asset_file.endswith('.uasset'):
                if check_starts_with(asset_file):
                    RELATIVE_PATH = _path.replace(USER_PATH, '')
                    output.append({
                        'type': asset_file.split('_')[0],
                        'name' : asset_file.split('.')[0],
                        'path' : os.path.join(RELATIVE_PATH, asset_file).replace('\\', '/').split('_')[0].replace(asset_file.split('_')[0], '').replace('Content/', 'Game/').replace('//', '/')
                    })
    with open(OUTPUT_PATH + 'BP_names_and_locations.json', 'w+') as file:
        json.dump(output, file, indent=2)

output()