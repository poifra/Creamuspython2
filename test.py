from __future__ import division
from Chordbook import transpose
from Sequencer import Sequence, Note
from Synth import ClassicSynth
from random import choice
from pyo import *

s = Server().boot()

#assuming 4/4 time
durees = {
	"whole":1,
	"half":1/2,
	"quarter":1/4,
	"eigth":1/8,
	"triple":1/12,
	"sixteenth":1/16,
}

scale =  transpose(target='minor', octave=6, key='G') + transpose(target='minor', octave=6, key='G')[::-1]

realNotes = [Note(i, durees["eigth"]) for i in scale]

seq = Sequence(realNotes,tempo=80)
syn = ClassicSynth(seq)

syn.sequence.play()
syn.get_out().out()

s.start()
s.gui(locals())
