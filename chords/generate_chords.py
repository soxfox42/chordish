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

# Based on a root of C, like MIDI.
# The choice is basically arbitrary though.
semitones = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

FILES = ["guitar", "ukulele"]

for file in FILES:
    with open(f"{file}.json") as f:
        data = json.load(f)

    chords = [{} for _ in range(12)] 
    for key, group in data["chords"].items():
        index = semitones[key[0]]
        if "sharp" in key or "#" in key:
            index += 1
        if "flat" in key or "b" in key:
            index -= 1
        index %= 12

        used_suffixes = []
        for chord in group:
            if chord["suffix"] not in SUFFIXES:
                continue
            used_suffixes.append(chord["suffix"])
            suffix = SUFFIXES[chord["suffix"]]
            frets = chord["positions"][0]["frets"]
            frets = [str(fret) if fret != -1 else "x" for fret in frets]
            chords[index][suffix] = "".join(frets)
        if len(used_suffixes) != len(SUFFIXES):
            print("Warning, unmatched suffixes")
    
    instruments[file] = chords


with open("../chord-definitions.typ", "w") as f:
    f.write("// Structure: chords > instrument > semitones-from-c > suffix\n")
    f.write("#let chords = (\n")
    for instrument, chords in instruments.items():
        f.write(f'  {instrument}: (\n')
        for group in chords:
            f.write(f'    (\n')
            for suffix, frets in group.items():
                f.write(f'      "{suffix}": "{frets}",\n')
            f.write(f'    ),\n')
        f.write(f'  ),\n')
    f.write(")\n")
