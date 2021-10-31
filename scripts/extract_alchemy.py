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
from functools import partial


def parse_function_value(text, name):
    # These functions use `.split(" ")` for some reason,
    # so we need to eval the return value to get the actual lists.
    return eval(re.search(rf"""{name}=function\(\){{return(.+?)}}""", text)[1])


def parse_bubble(bubble):
    parsed = {
        "name": bubble[0],
        "description": bubble[9].replace("_", " ").replace("{", "_"),
        "effect": bubble[-1],
        "powerPerLevel": float(bubble[1]),
        "algorithm": bubble[3],
        "materialNames": [item for item in bubble[5:8] if item != "Blank"],
    }

    try:
        parsed["materialCosts"] = [cost for cost in map(int, bubble[11:14]) if cost > 0]
    except (ValueError, IndexError):
        # Vials don't have costs, so they're 4 items shorter.
        # We only need to add costs for bubbles.
        pass

    return parsed


def parse_alchemy(path="Z.js"):
    with open(path, "r") as f:
        text = f.read()

    parse_z_fn = partial(parse_function_value, text)

    # The last category is the liquid shop, so don't parse it.
    categories = [
        list(map(parse_bubble, bubbles))
        for bubbles in parse_z_fn("AlchemyDescription")[:-1]
    ]

    return {
        "bubbles": dict(zip(["orange", "green", "purple", "yellow"], categories)),
        "vials": [
            vial | {"unlock": item, "roll": 100 - int(roll)}
            for vial, item, roll in zip(
                categories[-1],
                parse_z_fn("AlchemyVialItems"),
                parse_z_fn("AlchemyVialItemsPCT"),
            )
        ],
        "vialCosts": list(map(int, parse_z_fn("AlchemyVialQTYreq"))),
    }


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
            "used by the game to calculate power based on powerPerLevel and "
            "current level."
        )
    } | parse_alchemy(args.infile)

    with open("alchemy.json", "w") as f:
        json.dump(alchemy, f)
        print(f"Wrote to alchemy.json")
