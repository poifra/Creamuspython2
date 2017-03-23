from __future__ import division
from Chordbook import transpose
from Sequencer import Sequence, Note, Chord
from Synth import ClassicSynth
from random import choice
from pyo import *

s = Server().boot()

#scale =  transpose(target='minor', octave=6, key='F') + transpose(target='minor', octave=6, key='F')[::-1]

#realNotes = [Note(i, durees["eigth"]) for i in scale]

ii = transpose(target='minor triad', octave=5, key='G')
print ii

V = transpose(target='major triad', octave=5, key='C')
print V

I = transpose(target='major triad', octave=4, key='F')
print I

chrdSeq = [ii, V, I]
realChords = [Chord(i, durees['quarter']) for i in chrdSeq]
seq2 = Sequence(realChords, tempo=80)

#syn = ClassicSynth(seq)
syn2 = ClassicSynth(seq2)

syn2.sequence.play()
syn2.get_out().out()

s.start()
s.gui(locals())
