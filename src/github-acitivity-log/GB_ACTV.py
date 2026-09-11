import json
import sys
from os.path import exists
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

import requests


def main(user: str) -> None:
    """
    Main Thread of Activity Logger.
    :param user: github username
    :return: None
    """
    if str(input(fr"Do you wish to save {user}'s activity? Y\N: ")).upper() == "Y":
        save_file(user)

    # TODO: Console Output


def ask_directory() -> Path | None:
    """
    Asks User to selected desired save directory.
    Returns selected directory path or None if cancelled.
    :return Path | None: Directory path or None
    """
    root = Tk()
    try:
        root.withdraw()
        root.attributes('-topmost', True)
        selected = askdirectory(title='Select Folder',
                                mustexist=True,
                                parent=root)
    finally:
        root.destroy()

    if not selected:
        return None
    return Path(selected)


def build_filepath(path: Path, filename: str) -> Path:
    """This function cobines path and filename into a filepath
    or returns None if invalid.
    :param path: selected directory
    :param filename: name of the file
    :return Path | None: returns filepath or None if invalid
    """
    if isinstance(path, Path) and isinstance(filename, str):
        return path / filename
    else:
        raise ValueError(f"Following input: {path!r} and {filename!r} caused invalid filepath generation.")


def save_file(user: str) -> str:
    """
    Saves user's activity to a desired file.
    :param user: username:
    :return str: returns a message indicating whether the file was saved successfully
    """

    path = ask_directory()
    if path is None:
        return "User cancelled saving the activity."
    filename = str(input("Input filename: ")) + ".json"  # TODO: Filename correctness checks
    if (filepath := build_filepath(path, filename)) is None:
        raise ValueError("Filepath building went wrong.")

    if exists(f"{filepath}"):

        if (decision := str(input(r"Do you wish to overwrite the existing file? Y\N: ")).upper()) == "N":
            path = ask_directory()
            if path is None:
                return "User cancelled saving the activity."
            filename = str(input("Input filename: ")) + ".json"
            filepath = build_filepath(path, filename)
            if exists(f"{filepath}"):
                filename = filename[:-5] + "(1)" + filename[-5:]  # TODO: Fix - Collision suffix (1) is only tried once
        elif decision not in ["Y", "N"]:
            raise ValueError(f"Unexpected input provided: {decision!r}")

    with open(fr"{filepath}", "w") as f:
        json.dump(get_activity(user), f, indent=4)

    if exists(f"{filepath}"):
        print("successfully saved")
        return f"Successfully saved {user}'s activity"

    else:
        return f"Failed to save {user}'s activity"


def get_activity(user: str) -> list[dict] | dict:
    """
    Gets user's activity from github api
    :param user: github username
    :return: user's github activity in json format
    """
    r = requests.get(f"https://api.github.com/users/{user}/events")  # TODO: Add Status Checks
    return r.json()


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: main.py <username>")
    # TODO: Except ValueError in save_file()
