# PyTheory: Music Theory for Humans

This (work in progress) library attempt to make exploring music theory approachable to humans.

![logo](https://github.com/kennethreitz/pytheory/raw/master/ext/pytheory-small.png)

## True Scale -> Pitch Evaluation

```pycon
>>> from pytheory import TonedScale

>>> c_minor = TonedScale(tonic='C4')['minor']

>>> c_minor
<Scale I=C4 II=D4 III=Eb4 IV=F4 V=G4 VI=Ab4 VII=Bb5 VIII=C5>

>>> c_minor[0].pitch()
523.251130601197

>>> c_minor["I"].pitch(symbolic=True)
440*2**(1/4)

>>> c_minor["tonic"].pitch(temperament='pythagorean', symbolic=True)
14080/27
```

## Audibly play a note (or chord)

    >>> from pytheory import play
    play(c_minor[0], t=1_000)


## Chord Fingerings for Custom Tunings

```pycon
>>> from pytheory import Tone, Fretboard, CHARTS

>>> tones = (
...     Tone.from_string("F2"),
...     Tone.from_string("C3"),
...     Tone.from_string("G3"),
...     Tone.from_string("D4"),
...     Tone.from_string("A5"),
...     Tone.from_string("E5")
... )

>>> fretboard = Fretboard(tones=tones)
>>>
>>> c_chord = CHARTS['western']["C"]

>>> print(c_chord.fingering(fretboard=fretboard))
(0, 0, 0, 3, 3, 3)
```

It can also [generate charts for all known chords](https://gist.github.com/kennethreitz/b363660145064fc330c206294cff92fc) for any instrument (accuracy to be determined!).

✨🍰✨
