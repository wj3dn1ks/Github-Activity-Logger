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


def ask_directory() -> Path:
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = askdirectory(title='Select Folder')  # TODO: Folder not selected exception
    root.destroy()
    return Path(path)


def save_file(user: str) -> str:
    """
    Saves user's activity to a desired file.
    :param user: username:
    :return str: returns a message indicating whether the file was saved successfully
    """

    path = ask_directory()
    filename = str(input("Input filename: ")) + ".json"  # TODO: Filename correctness checks
    filepath = path / filename

    if exists(f"{filepath}"):

        if (decision := str(input(r"Do you wish to overwrite the existing file? Y\N: ")).upper()) == "N":
            path = ask_directory()
            filename = str(input("Input filename: ")) + ".json"
            if exists(f"{filepath}"):
                filename = filename[:-5] + "(1)" + filename[-5:]  #TODO: Fix - Collision suffix (1) is only tried once

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
    r = requests.get(f"https://api.github.com/users/{user}/events")  #TODO: Add Status Checks
    return r.json()


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: main.py <username>")
    #TODO: Except ValueError in save_file()
