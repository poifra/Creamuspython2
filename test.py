
from Chordbook import transpose, durations
from Sequencer import Sequence, Note
from Synth import ClassicSynth, BassWalkSynth
from random import choice
from pyo import *

s = Server().boot()
barCount = 0
noteCount = 0
scale =  transpose(target='m7', octave=3, key='G')
duree = durations["quarter"]
realNotes = [Note(i, duree) for i in scale]
seq = Sequence(realNotes,tempo=90)
syn = BassWalkSynth(seq)

syn.sequence.play()
syn.get_out().out()

def updateBarCount(dur):
	global barCount, noteCount
	if noteCount == 4:
		barCount += 1
		noteCount = 0
		print barCount
	noteCount += dur
p = Pattern(updateBarCount, duree, duree)
p.play()

s.start()
s.gui(locals())

# from random import choice, random
# from pyo import *
# from Chordbook import transpose

# from pyo import *

# s = Server().boot()
# SIZE = 4
# choices = transpose(target='major', octave=3)
# note = midiToHz(random.choice(choices))
# pick = Choice(midiToHz(choices),freq=2)
# port = SigTo(pick, time=0.01, mul = [1,1.005])
# vibrato = Sine(freq=1, mul=0.1)
# sig = SineLoop(freq=[port*(random.uniform(0.990,1.01)) for _ in range(SIZE)],feedback=0.1,mul=1.0/(5*SIZE)-vibrato)
# rev = Freeverb(sig,size=0.4, damp=1.0, bal=0.8).out()

# def change():
# 	note = midiToHz(random.choice(choices))
# 	sig.freq = [note*(random.uniform(0.990,1.01)) for _ in range(SIZE)]

# #p = Pattern(change, 0.25)
# #p.play()

# s.gui(locals())