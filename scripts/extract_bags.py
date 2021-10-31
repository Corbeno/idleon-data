#!/usr/bin/env python
"""Parses bags from Z.js. Run with --help for more info.

Input:
    * itemNames.json (created by extract_names.py) in the working directory.
    * Z.js (extracted from Idleon resources).
      Looks in the working directory by default,
      but the path can be passed in with --infile.

Output: bags.json in the working directory.

Requires Python 3.
"""

import json
import re
from argparse import ArgumentParser

pattern = re.compile(r"""PlayerCapacities=function\(\){return(.+?)}""")


def parse_bags(path="Z.js"):
    with open(path, "r") as f:
        text = f.read()

    with open("itemNames.json", "r") as f:
        names = json.load(f)

    # The function uses `.split(" ")`, so eval the return value to get the actual list.
    capacities = eval(pattern.search(text)[1])

    return {
        category: [
            {"index": bag[0], "id": bag[2], "name": names.get(bag[2], "FILLER")}
            for bag in bags
        ]
        for category, bags in zip(["inventory", "storage"], capacities)
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

    bags = {
        "__comment": (
            "Lists all bags in order by category. Includes placeholder bags "
            "that aren't in the game yet, indicated with the name 'FILLER'."
        ),
    } | parse_bags(args.infile)

    with open("bags.json", "w") as f:
        json.dump(bags, f)
        print(f"Wrote to bags.json")
