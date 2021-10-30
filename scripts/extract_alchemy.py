#!/usr/bin/env python
"""Parses alchemy from Z.js. Run with --help for more info.

Input: Z.js (extracted from Idleon resources).
       Looks in the working directory by default,
       but the path can be passed in with --infile.

Output: alchemy.json in the working directory.

Requires Python 3.
"""

import json
import re
from argparse import ArgumentParser

fn_pattern = r"""=function\(\){return(.+?)}"""


def parse_alchemy(path="Z.js"):
    with open(path, "r") as f:
        text = f.read()

    # These functions use `.split(" ")` for some reason,
    # so we need to eval the return value to get the actual lists.
    alchemy_description = eval(
        re.search(rf"""AlchemyDescription{fn_pattern}""", text)[1]
    )
    vial_items = eval(re.search(rf"""AlchemyVialItems{fn_pattern}""", text)[1])
    vial_percents = eval(re.search(rf"""AlchemyVialItemsPCT{fn_pattern}""", text)[1])

    # The 6th category is the liquid shop, which should probably be parsed separately.
    categories = ["orange", "green", "purple", "yellow", "vials"]

    alchemy = {
        category: [
            {
                "name": bubble[0],
                "powerPerLevel": float(bubble[1]),
                "algorithm": bubble[3],
                "materials": [item for item in bubble[5:8] if item != "Blank"],
                "description": bubble[9].replace("_", " ").replace("{", "_"),
                "effect": bubble[-1],
            }
            for bubble in bubbles
        ]
        for category, bubbles in zip(categories, alchemy_description)
    }

    # Add vial-specific info.
    alchemy["vials"] = [
        vial | {"unlock": item, "roll": 100 - int(roll)}
        for vial, item, roll in zip(alchemy["vials"], vial_items, vial_percents)
    ]

    return alchemy


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "infile",
        nargs="?",
        default="Z.js",
        help="path to Z.js (extracted from Legends of Idleon)",
    )
    args = parser.parse_args()

    alchemy = {
        "__comment": (
            "Contains all cauldron and vial data. Use itemNames.json to map "
            "material names to their display names. In descriptions, `_` is "
            "a placeholder for the current power. `algorithm` is the function "
            "used by the game to calculate power based on powerPerLevel "
            "and current level."
        )
    } | parse_alchemy(args.infile)

    with open("alchemy.json", "w") as f:
        json.dump(alchemy, f)
        print(f"Wrote to alchemy.json")
