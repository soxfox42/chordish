#import "chord-definitions.typ": chords as built-in

#let chord-state = state("chords", (
  transpose: 0,
  custom: (:),
))

#let define-chord(name, frets) = {
  chord-state.update(s => (..s, custom: s.custom + ((name): frets)))
}

#let chord-regex = regex("^(\\^?)([A-G])([#b])?(.*)$")

#let keys = (
  "C": 0,
  "D": 2,
  "E": 4,
  "F": 5,
  "G": 7,
  "A": 9,
  "B": 11,
)

#let key-list = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

#let get-chord(name) = {
  if type(name) == content {
    name = name.text
  }

  let current = chord-state.get()
  if name in current.custom {
    return (
      name: name,
      frets: current.custom.at(name),
    )
  }

  let match = name.match(chord-regex)
  if match == none {
    return none
  }

  let (prefix, key, accidental, kind) = match.captures
  let semitones = keys.at(key)
  if accidental == "#" {
    semitones += 1
  } else if accidental == "b" {
    semitones -= 1
  }
  semitones = calc.rem-euclid(semitones, 12)

  if current.transpose != 0 {
    semitones += current.transpose
    semitones = calc.rem-euclid(semitones, 12)

    name = prefix + key-list.at(semitones) + kind
  }

  return (
    name: name,
    frets: built-in.at(state("instrument").get()).at(semitones).at(kind),
  )
}
