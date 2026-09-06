import json
import sys
from os.path import exists

import requests


def main(user: str) -> None:
    """
    Dumps user's github activity into a {user}_activity.json file.
    :param user: github username
    :return: path to the generated JSON file
    """
    if exists(f"./{user}_activity.json"):
        if (decision := str(input(r"Do you wish to overwrite the existing file? Y\N: ")).upper()) == "N":
            raise FileExistsError("User decided not to overwrite the existing file.")
        elif decision not in ["Y", "N"]:
            raise ValueError(f"Unexpected input provided: {decision!r}")
    with open(f"{user}_activity.json", "w") as f:
        json.dump(get_info(user), f, indent=4)


def get_info(user: str) -> str:
    """
    Gets user's activity from github api
    :param user: github username
    :return: user's github activity in json format
    """
    r = requests.get(f"https://api.github.com/users/{user}/events")
    return r.json()


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: main.py <username>")
