import json

SUFFIXES = {
    "major": "",
    "minor": "m",
    "7": "7",
    "7sus4": "7sus4",
    "m7": "m7",
    "dim": "dim",
    "maj7": "maj7",
    "6": "6",
    "sus2": "sus2",
    "sus4": "sus4",
    "aug": "aug",
    "m6": "m6",
    "9": "9",
}

instruments = {}

FILES = ["guitar", "ukulele"]

for file in FILES:
    with open(f"{file}.json") as f:
        data = json.load(f)

    chords = {}
    for group in data["chords"].values():
        used_suffixes = []
        for chord in group:
            if chord["suffix"] not in SUFFIXES:
                continue
            used_suffixes.append(chord["suffix"])
            name = chord["key"] + SUFFIXES[chord["suffix"]]
            frets = chord["positions"][0]["frets"]
            frets = [str(fret) if fret != -1 else "x" for fret in frets]
            chords[name] = "".join(frets)
        if len(used_suffixes) != len(SUFFIXES):
            print("Warning, unmatched suffixes")
    
    instruments[file] = chords


with open("../songbook/chords.typ", "w") as f:
    f.write("#let chords = (\n")
    for instrument, chords in instruments.items():
        f.write(f'    {instrument}: (\n')
        for name, frets in chords.items():
            f.write(f'        "{name}": "{frets}",\n')
        f.write(f'    ),\n')
    f.write(")\n")
