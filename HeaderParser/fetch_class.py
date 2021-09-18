import os, shutil, re
from Config import Config

config = Config()


def strip_name(classname: str):
    return classname.split(".")[0].lower()


def find_class_path_and_name(classname: str, in_path: str = config.OUTPUT_DIR) -> (str, str):
    classname = strip_name(classname)
    for root, dirs, files in os.walk(in_path):
        for name in files:
            realname = name.split(".")[0]
            if realname.lower() == classname:
                return os.path.join(root, realname), realname


def try_fetch_class(classname: str) -> (str, str) or None:
    path, name = find_class_path_and_name(classname)
    if path is None:
        return
    to_path = os.path.join(config.FETCH_DIR, name)
    os.makedirs(to_path, True)
    shutil.copy(path + ".h", to_path)
    #shutil.copy(path + ".cpp", to_path)  # TODO: enable
    return os.path.join(to_path, name + ".h"), name


def fetch_parents(header_path: str, have: list[str]):
    inc = re.search(r"--- automatic includes ---\n(?P<includes>(?:.|\n)*)\n\/\/ --------------------------\n",
                    open(header_path).read()).group("includes")
    count = 0
    for match in re.finditer(r'#include "(?P<class>.*)"', inc):
        if strip_name(match.group("class")) in have:
            continue
        path, name = try_fetch_class(match.group("class"))
        count += 1
        have.append(strip_name(name))
        count += fetch_parents(path, have)
    return count



if __name__ == '__main__':
    while True:
        print("Which class would you like to fetch?")
        #name = input(" > ")
        name = "fsdgamestate"
        shutil.rmtree(config.FETCH_DIR, True)
        path, name = try_fetch_class(name)
        if path is None:
            print("Not found!")
            continue
        parent_count = fetch_parents(path, [strip_name(name)])
        print(f"Fetched {name} and its {parent_count} included parent classes.")

        break



