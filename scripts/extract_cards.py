#!/usr/bin/env python
"""Parses cards from Z.js. Run with --help for more info.

Input: Z.js (extracted from Idleon resources).
       Looks in the working directory by default,
       but the path can be passed in with --infile.

Output: cards.json in the working directory.

Requires Python 3.
"""

import json
import re
from argparse import ArgumentParser

pattern = re.compile(r"""CardStuff=function\(\){return(.+?)}""")


def parse_cards(path="Z.js"):
    with open(path, "r") as f:
        text = f.read()

    cardstuff = json.loads(pattern.search(text)[1])
    return [
        [
            {
                "name": name,
                "id": id_,
                "amountPerTier": float(amount),
                "effect": effect.lstrip("+{").replace("_", " "),
                "powerPerTier": float(power),
            }
            for name, id_, amount, effect, power in category
        ]
        for category in cardstuff
    ]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "infile",
        nargs="?",
        default="Z.js",
        help="path to Z.js (extracted from Legends of Idleon)",
    )
    args = parser.parse_args()

    cards = {
        "__comment": (
            "Lists all cards in order by category. Category names are not in Z.js, "
            "so users will need to maintain their own list of card category names. "
            "Use monsterNames.json to map the card names to their display names. "
            "The full card bonus text takes the form `+<powerPerTier*tier><effect>`; "
            "leading spaces are left in for consistency between flat and percentage "
            "bonuses. Blank cards are placeholders for empty spaces in the UI."
        ),
        "data": parse_cards(args.infile),
    }

    with open("cards.json", "w") as f:
        json.dump(cards, f)
