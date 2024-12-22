#import "chord-definitions.typ": chords as built-in

#let custom-chords = state("custom-chords", (:))
#let define-chord(name, frets) = {
  custom-chords.update(c => c + ((name): frets))
}

#let get-chord(name) = {
  if type(name) == content {
    name = name.text
  }

  if name in custom-chords.get() {
    return custom-chords.get().at(name)
  }
  built-in.at(state("instrument").get()).at(name, default: none)
}
