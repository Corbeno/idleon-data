#!/usr/bin/env python
"""Parses names from Z.js. Run with --help for more info.

Input: Z.js (extracted from Idleon resources).
       Looks in the working directory by default,
       but the path can be passed in with --infile.

Output: itemNames.json and monsterNames.json in the working directory.
        The format is JSON by default, but can be changed with --format.

Requires Python 3.9+.
"""

import csv
import json
import re
from argparse import ArgumentParser

VALID_VAR = r"[$\w]+"  # Minified variable name
VALID_STR = r".+?"  # The actual character set is [|.'\-\w], but . works fine for now

internal_pattern = re.compile(
    rf"""
    addNew\w+\("({VALID_STR})"  # Match any addNew___ function
    ,{VALID_VAR}\)  # Exclude monster definitions, which contain an object
                    # instead of a variable and have no associated displayName
                    # (must be parsed separately)
    """,
    re.X,
)
display_pattern = re.compile(rf'''setReserved\("displayName","({VALID_STR})"''')
monster_pattern = re.compile(
    rf'''addNewMonster\("({VALID_STR})",{{Name:"({VALID_STR})"'''
)
whitespace_pattern = re.compile(r"[_|]+")


def get_text(path="Z.js"):
    with open(path, "r") as f:
        return f.read().replace(";", "\n")


def parse_names(path="Z.js"):
    text = get_text(path)

    print("Finding names...")
    internal_names = internal_pattern.findall(text)
    print(f"{len(internal_names)} internal names found")
    display_names = display_pattern.findall(text)
    print(f"{len(display_names)} display names found")

    if len(display_names) != len(internal_names):
        raise ValueError(
            "Display names should pair one-to-one with internal names, but there was a mismatch. "
            f"Found {len(display_names)} display names and {len(internal_names)} internal names."
        )

    # Condense all whitespace (_ and |) into a single space
    display_names = [whitespace_pattern.sub(" ", name) for name in display_names]

    return dict(zip(internal_names, display_names))


def parse_monsters(path="Z.js"):
    text = get_text(path)

    # Condense all whitespace (_ and |) into a single space
    return {
        internal: whitespace_pattern.sub(" ", display)
        for internal, display in monster_pattern.findall(text)
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--infile",
        default="Z.js",
        help="path to Z.js (extracted from Legends of Idleon)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "csv"],
        default="json",
        help="format of output files",
    )
    args = parser.parse_args()

    datafiles = {
        "itemNames": {
            "__comment": (
                "Maps the item names stored in the game code to those "
                "displayed in-game. This contains every inventory item in the game."
            )
        }
        | parse_names(args.infile),
        "monsterNames": {
            "__comment": (
                "Maps the monster names stored in the game code to those "
                "displayed in-game. This also includes interactable objects."
            )
        }
        | parse_monsters(args.infile),
    }

    for name, data in datafiles.items():
        filename = f"{name}.{args.format}"

        with open(filename, "w", newline="") as f:
            if args.format == "json":
                json.dump(data, f)
            elif args.format == "csv":
                writer = csv.writer(f)
                writer.writerow(["Internal", "Display"])
                writer.writerows(data.items())
            else:
                raise ValueError(
                    f"Invalid output format '{args.format}'. Valid formats: json, csv"
                )

            print(f"Wrote to {filename}")
