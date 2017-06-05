
from Chordbook import transpose, durations
from Sequencer import Sequence, Note
from Synth import ClassicSynth, BassWalkSynth, PianoSynth
from random import choice
from itertools import cycle
from pyo import *

s = Server().boot()
noteCount = 1
totalCount = 0
tempo = 70
chords = cycle(
		[
		transpose(target='m7',key='D',octave=5),
		transpose(target='7',key='G',octave=5),
		transpose(target='maj7', key='C',octave=5)
		]
	)
chordName = cycle(['Dm7','G7','CMaj7'])
currentChord = next(chords)
currentChordName = next(chordName)
duree = durations['half']

realNotes = [Note(n, duree) for n in currentChord]
seqs = [Sequence([n],tempo) for n in realNotes]

for seq in seqs:
	seq.play()

synths = [PianoSynth(seq) for seq in seqs]

for syn in synths:
	syn.get_out().out()

def changeChord():
	global currentChord, seqs, synths
	global noteCount, currentChordName, totalCount
	if noteCount > 4:
		print "changing chord"
		noteCount = 1
		currentChord = next(chords)
		currentChordName = next(chordName)
		newNotes = [Note(n, duree) for n in currentChord]
		for seq in seqs:
			if seq.isPlaying():
				seq.stop()

		seqs = [Sequence([n],tempo) for n in newNotes]
		synths = [PianoSynth(seq) for seq in seqs]

	for seq in seqs:
		if not(seq.isPlaying()):
			seq.play()

	for syn in synths:
		syn.get_out().out()
	print "Current="+currentChordName+" Total count="+str(totalCount)
	noteCount += 1
	totalCount += 1

pat = Pattern(changeChord, time=60/(tempo / durations['quarter'] / 4))
pat.play()
s.gui(locals())
