import json
import sys
from json import JSONDecodeError
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

    data = get_activity(user)
    if not data:
        print(f"No activity found for user: {user}")
    else:
        save_file(user, data)

    # TODO: Console Output


def ask_directory(ask_title: str | None = "Select Directory") -> Path | None:
    """
    Asks User to selected desired save directory.
    Returns selected directory path or None if cancelled.
    :return Path | None: Directory path or None
    """
    root = Tk()
    try:
        root.withdraw()
        root.attributes('-topmost', True)
        selected = askdirectory(title=ask_title,
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


def save_file(user: str, data: list[dict] | dict | None) -> str:
    # TODO: Separate this function into many smaller ones
    """
    Saves user's activity to a desired file.
    :param user: username
    :param data: user's activity data
    :return str: returns a message indicating whether the file was saved successfully
    """

    path = ask_directory()
    if path is None:
        return "User cancelled saving the activity."
    filename = str(input("Input filename: ")) + ".json"  # TODO: Filename correctness checks
    filepath = build_filepath(path, filename)
    # code above is the 1st filepath building attempt

    if exists(filepath):
        if (decision := str(input(r"Do you wish to overwrite the existing file? Y\N: ")).upper()) == "N":
            # asks user to point a new directory and filepath
            path = ask_directory()
            if path is None:
                return "User cancelled saving the activity."
            filename = str(input("Input filename: ")) + ".json"
            filepath = build_filepath(path, filename)
        elif decision not in ["Y", "N"]:
            raise ValueError(f"Unexpected input provided: {decision!r}")

    # adds suffix if the file already exists AGAIN
    while exists(filepath):
        try:
            if isinstance(int(filename[-7:-6]), int):  # I might change slicing to regex someday
                filename = filename[:-7] + str(int(filename[-7:-6]) + 1) + filename[-6:]
        except ValueError:
            filename = filename[:-5] + "(1)" + filename[-5:]
        filepath = build_filepath(path, filename)

    # writes the data to the file, runs error checks
    try:
        with open(filepath, "w", encoding="utf-8") as f:  # TODO: write the data to a temp file first, then replace
            json.dump(data, f, indent=4)
    except (OSError, TypeError) as e:
        raise RuntimeError(f"Failed to save {user}'s activity. Error: {e}") from e

    try:
        with open(filepath, "r") as f:
            json.load(f)
    except (JSONDecodeError, OSError) as e:
        raise RuntimeError(f"File is corrupted. Error: {e}") from e

    return "File saved successfully at: " + str(filepath)


def get_activity(user: str) -> list[dict]:
    """
    Gets user's activity from github api
    :param user: github username
    :return: user's github activity in json format
    """

    # TODO: make this more catch-all, specific handling where needed

    try:
        r = requests.get(f"https://api.github.com/users/{user}/events", timeout=15)
        #TODO: make the GET API request follow GitHb REST conventions
        r.raise_for_status()
    except requests.exceptions.Timeout as e:
        raise RuntimeError(f"Request timed out for: '{user}'") from e
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"GitHub API request failed for '{user}', error: {e}") from e
    else:
        return r.json()


if __name__ == "__main__":
    try:
        main(sys.argv[1])  # TODO: Add username Check
    except IndexError:
        print("current WIP usage: python __init__.py <username>")
    # TODO: Except ValueError in save_file()
