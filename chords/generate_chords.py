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
KEY_LIST = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_to_semitone(note):
    index = KEY_LIST.index(note[0])
    if "sharp" in note or "#" in note:
        index += 1
    if "flat" in note or "b" in note:
        index -= 1
    return index % 12


FILES = ["guitar", "ukulele", "mandolin"]

for file in FILES:
    with open(f"{file}.json") as f:
        data = json.load(f)

    chords = [{} for _ in range(12)]
    for key, group in data["chords"].items():
        index = note_to_semitone(key)

        used_suffixes = []
        for chord in group:
            raw_suffix = chord["suffix"]
            if raw_suffix in SUFFIXES:
                used_suffixes.append(raw_suffix)
                suffix = SUFFIXES[raw_suffix]
            elif "/" in raw_suffix:
                kind, bass = raw_suffix.split("/", 1)
                if kind not in SUFFIXES.values():
                    continue
                # Force all slash chords to be stored as sharps
                bass_name = KEY_LIST[note_to_semitone(bass)]
                suffix = f"{kind}/{bass_name}"
            else:
                continue
            position = chord["positions"][0]
            frets = position["frets"]
            for i, fret in enumerate(frets):
                if fret != -1:
                    frets[i] += position["baseFret"] - 1
            has_high_fret = any(fret >= 10 for fret in frets)
            frets = [str(fret) if fret != -1 else "x" for fret in frets]
            if has_high_fret:
                fret_string = ",".join(frets)
            else:
                fret_string = "".join(frets)
            chords[index][suffix] = fret_string
        if len(used_suffixes) != len(SUFFIXES):
            print("Warning, unmatched suffixes")

    instruments[file] = chords


with open("../chord-definitions.typ", "w") as f:
    f.write("// Structure: chords > instrument > semitones-from-c > suffix\n")
    f.write("#let chords = (\n")
    for instrument, chords in instruments.items():
        f.write(f"  {instrument}: (\n")
        for group in chords:
            f.write(f"    (\n")
            for suffix, frets in group.items():
                f.write(f'      "{suffix}": "{frets}",\n')
            f.write(f"    ),\n")
        f.write(f"  ),\n")
    f.write(")\n")
