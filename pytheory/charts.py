import itertools

from .systems import SYSTEMS
from .tones import Tone

QUALITIES = ('', 'maj', 'm', '5', '7', '9', 'dim', 'm6', 'm7', 'm9', 'maj7', 'maj9')
MAX_FRET = 7

CHARTS = {}
CHARTS['western'] = []

class NamedChord:
    def __init__(self, *, tone_name, quality):
        self.tone_name = tone_name
        self.quality = quality

    @property
    def name(self):
        return f"{self.tone_name}{self.quality}"

    @property
    def tone(self):
        return Tone(name=self.tone_name)

    def __repr__(self):
        return f"<NamedChord name={self.name!r}>"

    @property
    def acceptable_tones(self):
        acceptable = [self.tone]


        # Major third.
        if self.quality == 'maj':
            acceptable += [self.tone.add(3)]

        # Minor third.
        elif self.quality == 'm':
            acceptable += [self.tone.add(4)]

        # Perfect fifth.
        elif self.quality == '5':
            acceptable += [self.tone.add(5)]

        elif self.quality == '7':
            acceptable += [self.tone.add(7)]

        elif self.quality == '9':
            acceptable += [self.tone.add(9)]

        elif self.quality == 'dim':
            acceptable += [self.tone.add(4), self.tone.add(8)]

        elif self.quality == 'm6':
            acceptable += [self.tone.add(4), self.tone.add(6)]

        elif self.quality == 'm7':
            acceptable += [self.tone.add(4), self.tone.add(7)]
            
        elif self.quality == 'm9':
            acceptable += [self.tone.add(4), self.tone.add(9)]

        elif self.quality == 'maj7':
            acceptable += [self.tone.add(3), self.tone.add(7)]
            
        elif self.quality == 'maj9':
            acceptable += [self.tone.add(3), self.tone.add(9)]

        else:
            acceptable += [self.tone.add(5)]
            acceptable += [self.tone.subtract(5)]

        return tuple(acceptable)

    @property
    def acceptable_tone_names(self):
        return tuple([tone.name for tone in self.acceptable_tones])

    def _possible_fingerings(self, *, fretboard):
        def find_fingerings(tone):
            fingerings = []
            for j in range(MAX_FRET):
                fingered_tone = tone.add(j)
                for acceptable_tone in self.acceptable_tones:
                    if fingered_tone.name == acceptable_tone:
                        fingerings.append(j)

            return tuple(fingerings)

        fingering = []
        for i, tone in enumerate(fretboard.tones):
            fingering.append(find_fingerings(tone))

        for i, finger in enumerate(fingering):
            if finger == ():
                fingering[i] = (-1,)

        return tuple(fingering)

    @staticmethod
    def fix_fingering(fingering):
        fingering = list(fingering)
        for i, finger in enumerate(fingering):
            if finger == -1:
                fingering[i] = None
        return tuple(fingering)

    def fingerings(self, *, fretboard):
        return tuple(itertools.product(*self._possible_fingerings(fretboard=fretboard)))

    def fingering(self, *, fretboard, multiple=False):
        def fingering_score(fingering):
            def number_of_fingers(fingering):
                zeros = 0
                for finger in fingering:
                    if finger == 0:
                        zeros += 1
                return len(fingering) - zeros

            def ascending(fingering):
                fingering = [f for f in fingering if f != 0]

                return sorted(fingering) == fingering

            ascending = int(ascending(fingering))
            finger_count = number_of_fingers(fingering)
            return ascending + (1 / finger_count)

        def gen():
            fingerings = self.fingerings(fretboard=fretboard)
            score_map = tuple(map(fingering_score, fingerings))
            max_score = max(score_map)

            for possible_fingering in fingerings:
                if fingering_score(possible_fingering) == max_score:
                    yield possible_fingering

        best_fingerings = tuple([g for g in gen()])
        if not multiple:
            return self.fix_fingering(best_fingerings[0])
        else:
            return tuple([self.fix_fingering(f) for f in best_fingerings])



western_chart = {}
for tone_titles in SYSTEMS['western'].tone_names:
    # Take the second tone name, if it's available.
    if len(tone_titles) == 2:
        tone_name = tone_titles[1]
    else:
        tone_name = tone_titles[0]

    for quality in QUALITIES:
        named_chord = NamedChord(tone_name=tone_name, quality=quality)
        western_chart.update({f"{tone_name}{quality}": named_chord})

CHARTS['western'] = western_chart

def charts_for_fretboard(*, chart=CHARTS['western'], fretboard):
    super_chart = {}
    for chord in chart:
        super_chart[chord] = chart[chord].fingering(fretboard=fretboard)
    return super_chart
