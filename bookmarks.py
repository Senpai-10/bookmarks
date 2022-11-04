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
from notifypy import Notify

commands = ["add", "remove", "find"]

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


def main(command: str):
    list_of_bookmarks = manage_bookmarks.load("~/bookmarks.txt") or {}

    match command:
        case "add":
            create_new_category_text = "new category!"

            category = (
                dmenu.show(
                    list(list_of_bookmarks.keys()) + [create_new_category_text],
                    prompt="Select a category: ",
                )
                or create_new_category_text
            )

            bookmark = get_selected_text()

            if category == create_new_category_text:
                category = dmenu.input("New category: ")

            list_of_bookmarks.setdefault(category, []).append(bookmark)

            notification.title = f"New bookmark added to {category}"
            notification.message = f"{bookmark}"
            notification.send()

            manage_bookmarks.write_back("~/bookmarks.txt", list_of_bookmarks)

        case "remove":
            category = dmenu.show(
                list(list_of_bookmarks.keys()),
                prompt="Select a category: ",
            )

            if category == None:
                return

            bookmarks = list_of_bookmarks.get(category) or []

            if len(bookmarks) == 0:
                return

            bookmark = dmenu.show(bookmarks)

            bookmarks.remove(bookmark)

            manage_bookmarks.write_back("~/bookmarks.txt", list_of_bookmarks)

        case "find":
            category = dmenu.show(
                list(list_of_bookmarks.keys()),
                prompt="Select a category: ",
            )

            if category == None:
                return

            bookmarks = list_of_bookmarks.get(category) or []

            if len(bookmarks) == 0:
                return

            bookmark = dmenu.show(bookmarks)

            if bookmark == None: return

            args = ["xclip", "-selection", "clipboard"]

            process = subprocess.Popen(["echo", bookmark], stdout=subprocess.PIPE)

            subprocess.Popen(
                args,
                stdin=process.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

        # case _:
        #     print("unknown command!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="bookmarks",
        description="simple bookmarks manager",
    )

    parser.add_argument("-c", "--cmd", type=str, choices=commands, required=False)

    opts = parser.parse_args()

    cmd = opts.cmd

    if cmd is None:
        cmd = dmenu.show(commands, prompt="select command") or ""

    main(cmd)
