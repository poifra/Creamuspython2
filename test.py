from __future__ import division
from Chordbook import transpose
from Sequencer import Sequence, Note
from Synth import ClassicSynth
from random import choice
from pyo import *

s = Server().boot()
durees = {
	"whole":1,
	"half":0.5,
	"quarter":0.25,
	"eigth":0.125,
	"sixteenth":0.0625
}
realNotes = [Note(i, durees["sixteenth"]) for i in transpose(target='minor', octave=6, key='G')]
seq = Sequence(realNotes,tempo=60)
syn = ClassicSynth(seq)

syn.sequence.play()
syn.get_out().out()

s.start()
s.gui(locals())
