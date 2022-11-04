#!/bin/env python

"""
interface to select bookmark or add or remove
    show categories first and if (add) make the first item in list "+create new category"
    when category is select if (
            remove or find
    ) show all bookmarks in category

hown to save bookmark?

bookmarks file:

CATEGORY default is other_bookmarks
CATEGORY name sould not have a space!

CATEGORY BOOKMARK
"""

import argparse
from bookmarks_lib import dmenu
from bookmarks_lib import manage_bookmarks
import subprocess
from enum import Enum
from notifypy import Notify


class Commands(Enum):
    add = "add"
    remove = "remove"
    find = "find"

    def __str__(self):
        return self.value


notification = Notify()

notification.icon = ""


def get_selected_text():
    args = ["xclip", "-o"]

    proc = subprocess.Popen(
        args,
        universal_newlines=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert proc.stdout is not None
    assert proc.stderr is not None

    return proc.stdout.read().rstrip("\n")


def main(command: Commands):
    match command:
        case command.add:
            list_of_bookmarks = manage_bookmarks.load("~/bookmarks.txt") or {}
            create_new_category_text = "new category!"

            category = dmenu.show(
                list(list_of_bookmarks.keys()) + [create_new_category_text],
                prompt="Select a category: ",
            ) or create_new_category_text

            bookmark = get_selected_text()

            if category == create_new_category_text:
                category = dmenu.input("New category: ")

            list_of_bookmarks.setdefault(category, []).append(bookmark)

            notification.title = f"New bookmark added to {category}"
            notification.message = f"{bookmark}"
            notification.send()

            manage_bookmarks.write_back("~/bookmarks.txt", list_of_bookmarks)

        case command.remove:
            ...

        case command.find:
            ...

        # case _:
        #     print("unknown command!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="bookmarks",
        description="simple bookmarks manager",
    )

    parser.add_argument("command", type=Commands, choices=list(Commands))

    opts = parser.parse_args()

    main(opts.command)
