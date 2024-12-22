#import "chord-definitions.typ": chords as built-in

#let custom-chords = state("custom-chords", (:))
#let define-chord(name, frets) = {
  custom-chords.update(c => c + ((name): frets))
}

#let chord-regex = regex("^\\^?([A-G])([#b])?(.*)$")

#let keys = (
  "C": 0,
  "D": 2,
  "E": 4,
  "F": 5,
  "G": 7,
  "A": 9,
  "B": 11,
)

#let chord-name(text) = {
  text.match(chord-regex).captures.join()
}

#let get-chord(name) = {
  if type(name) == content {
    name = name.text
  }

  if name in custom-chords.get() {
    return custom-chords.get().at(name)
  }

  let match = name.match(chord-regex)
  if match == none {
    return none
  }

  let (key, accidental, kind) = match.captures
  let semitones = keys.at(key)
  if accidental == "#" {
    semitones += 1
  } else if accidental == "b" {
    semitones -= 1
  }
  semitones = calc.rem-euclid(semitones, 12)

  built-in.at(state("instrument").get()).at(semitones).at(kind)
}
