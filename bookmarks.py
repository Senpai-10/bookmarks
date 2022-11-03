#!/bin/env python

'''
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
'''

import argparse
import bookmarks_lib.dmenu as dmenu
from enum import Enum


class Commands(Enum):
    add = "add"
    remove = "remove"
    find = "find"

    def __str__(self):
        return self.value

from notifypy import Notify

notification = Notify()

notification.icon = ""


def main(command: Commands):
    match command:
        case command.add:
            notification.send()
            print(dmenu.input("hi"))
            dmenu.show(["hi", "hi2", "hi3"])

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
