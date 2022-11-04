""" Load bookmarks from bookmarks file

file:

CATEGORY BOOKMARK
"""

from os import path
from typing import Dict


def load(file_path: str) -> Dict[str, list] | None:
    file_path = path.expanduser(file_path)

    mylist: Dict[str, list] = {}

    if path.exists(file_path) == False:
        print(f"'{file_path}' does not exists!")
        return None

    if path.isdir(file_path):
        print(f"'{file_path}' is not a file!")
        return None

    with open(file_path, mode="r") as f:
        for line in f.readlines():
            if ";" in line:
                line = line.split(";", 1)

                category = line[0]
                bookmark = line[1].rstrip("\n")

                # Remove duplicated bookmarks in the same category
                tmp_list = mylist.get(category)
                if tmp_list != None and bookmark in tmp_list:
                    continue

                # create empty array of key (category) is not found
                mylist.setdefault(category, []).append(bookmark)

    return mylist


def write_back(file_path: str, list_of_bookmarks: Dict[str, list]):
    file_path = path.expanduser(file_path)
    file_content = ""

    for key in list_of_bookmarks.keys():
        bookmarks = list_of_bookmarks[key]

        for bookmark in bookmarks:
            file_content += f"{key};{bookmark}\n"

    with open(file_path, "w") as f:
        f.write(file_content)
