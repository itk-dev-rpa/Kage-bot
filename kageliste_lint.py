import yaml
import sys

KNOWN_NAMES = [
    "Gitte",
    "Mathias",
    "Ture",
    "Lene",
    "Line",
    "Jeppe KA",
    "Mikkel",
    "Kristian",
    "Jesper P",
    "Anna",
    "Mads",
    "Jeppe",
    "Martin",
    "Jesper K"
]


with open("kageliste.yaml") as file:
    data = yaml.safe_load(file)


for year in data:
    for week, person in data[year].items():
        if person and person not in KNOWN_NAMES:
            print(f"{person} is not on the known list of names!")
            sys.exit(1)


print("Done")