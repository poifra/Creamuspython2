from __future__ import division

from Sequencer import Sequence, Note
from itertools import cycle
from Synth import BaseSynth, ClassicSynth, BassWalkSynth, PianoSynth
from pyo import *
from AudioEngine import WalkingBass
from Chordbook import durations, changeOctave

class AudioPlayer():
	def __init__(self, tempo, chords, chordNames, key, verbose = True):
		self.serv = Server().boot()
		self.bassWalk = WalkingBass(chords, key)
		self.bassWalk.buildWalkingBass()
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.currentNote = 1
		self.noteCounter = Pattern(self._timer,self.dur)
		self.setChords(chords, firstTime = True, cNames = chordNames)
		self.firstChord = self.currentChord
		self.totalCount = 1
		self.verbose = verbose
		self.serv.gui(locals())

	def play(self, tempo):
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.noteCounter.setTime(self.dur)
		self.noteCounter.play()
		self.serv.start()

	def stop(self):
		if self.bassSeq.isPlaying:
			self.bassSeq.stop()
		for seq in self.chordSeqs:
			if seq.isPlaying:
				seq.stop()

		self.currentNote = 1
		self.currentChord = self.firstChord
		self.currentBass
		self.noteCounter.stop()
		self.serv.stop()

	def setTempo(self, tempo):
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.noteCounter.time = self.dur

	def setKey(self, key):
		self.bassWalk.validateKey(key)
		self.key = key

	def setChords(self, chords, firstTime = False, cNames = None):
		print "in setChords",cNames
	
		self.chords = []
		self.bassNotes = []

		bassline = self.bassWalk.getBassline()
		#convert bassline to a list of lists, where each sublist is a bar
		bassBlocks = [bassline[i:i+4] for i in range(0,len(bassline),4)]

		for i,c in enumerate(chords):
			self.chords.append(changeOctave(c,amount=2))
			self.bassNotes.append(bassBlocks[i])

		self.chords = cycle(self.chords)
		self.bassNotes = cycle(self.bassNotes)
		self.chordNames = cycle(cNames)
		
		self.currentChord = next(self.chords)
		self.currentBass = next(self.bassNotes)
		self.currentName = next(self.chordNames)
		
		self._regenerateMusic(firstTime)

	def _regenerateMusic(self, firstTime = False):
		newBass = [Note(n, self.dur) for n in self.currentBass]
		newChord = [Note(n, self.dur*2) for n in self.currentChord]
		
		if firstTime:
			self._createSynths(newBass, newChord)
		else:
			if self.bassSeq.isPlaying():
				self.bassSeq.stop()
			for seq in self.chordSeqs:
				if seq.isPlaying:
					seq.stop()
			self._createSynths(newBass, newChord)
		self.bassSynth.get_out().out()
		if not(self.bassSeq.isPlaying()):
			self.bassSeq.play()

		for s in self.chordSynths:
			s.get_out().out()
		for seq in self.chordSeqs:
			if not(seq.isPlaying()):
				seq.play()

	def _createSynths(self, newBass, newChord):
		self.bassSeq = Sequence(newBass, self.tempo)
		self.bassSynth = PianoSynth(self.bassSeq)
		self.chordSeqs = [Sequence([note],self.tempo) for note in newChord]
		self.chordSynths = [ClassicSynth(c,amp=0.1) for c in self.chordSeqs]

	def _timer(self):
		if self.currentNote > 4:
			self.currentChord = next(self.chords)
			self.currentName = next(self.chordNames)
			self.currentBass = next(self.bassNotes)
			self._regenerateMusic()
			self.currentNote = 1

		if self.verbose:
			print "Current note="+str(self.currentNote)+" Total count="+str(self.totalCount)
			print "Current Chord="+str(self.currentName)
		self.currentNote += self.dur
		self.totalCount += 1