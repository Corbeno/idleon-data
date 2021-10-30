#!/usr/bin/env python
"""Collects some item names into auxiliary data files.

Input: itemNames.json (created by extract_names.py) in the working directory.

Output: stampList.json, statueList.json, bagNames.json in the working directory.

Requires Python 3.9+.
"""

import json

with open("itemNames.json", "r") as f:
    names = json.load(f)


def filter_startswith(prefix):
    return {k: v for k, v in names.items() if k.startswith(prefix)}


datas = {
    "stampList": {
        "__comment": (
            "Lists all stamps in order by category. "
            "Preserves placeholders to keep indexes consistent."
        )
    }
    | {
        category: list(filter_startswith(f"Stamp{letter}").values())
        for category, letter in zip(("Combat", "Skill", "Misc"), "ABC")
    },
    "statueList": {
        "__comment": "Lists all statues in order.",
        "data": list(filter_startswith("EquipmentStatues").values()),
    },
    "bagNames": {
        "__comment": "Lists all bags in order by category.",
        "inventory": filter_startswith("InvBag"),
        "storage": filter_startswith("InvStorage"),
    },
}

for name, data in datas.items():
    filename = f"{name}.json"
    with open(filename, "w") as f:
        json.dump(data, f)
        print(f"Wrote to {filename}")
