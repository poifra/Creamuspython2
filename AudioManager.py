from Sequencer import Sequence, Note
from itertools import cycle
from Synth import BaseSynth, ClassicSynth, BassWalkSynth
from pyo import *
from Chordbook import durations

class AudioPlayer():
	def __init__(self, tempo, chords, chordNames, verbose = True):
		self.serv = Server().boot()
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.currentNote = 1
		self.noteCounter = Pattern(self._timer,self.dur)
		
		self.chords = cycle(chords)
		self.chordNames = cycle(chordNames)
		self.verbose = verbose

		self.currentBar = next(self.chords)
		self.currentName = next(self.chordNames)
		self.firstChord = self.currentBar
		self._regenerateMusic()

	def play(self, tempo):
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.noteCounter.setTime(self.dur)
		self.noteCounter.play()
		self.serv.start()

	def stop(self):
		self.currentNote = 1
		self.currentBar = self.firstChord
		self.noteCounter.stop()
		self.serv.stop()

	def setChords(self, chords, chordNames = None):
		self.chords = cycle(chords)
		self.currentNote = 1
		self.currentBar = next(self.chords)
		self.firstChord = self.currentBar

	def _regenerateMusic(self):
		realBass = [Note(n, durations['quarter']) for n in self.currentBar]
		realChord = [Note(n, durations['half']) for n in self.currentBar]
		bassSeq = Sequence(realBass, self.tempo)
		self.bassSynth = BassWalkSynth(bassSeq)
		self.bassSynth.out()

		chord = [Sequence([note],self.tempo) for note in realChord]
		self.chordSynths = [ClassicSynth(c) for c in chord]
		for s in self.chordSynths:
			s.out()

	def _timer(self):
		if self.currentNote > 4:
			self.currentBar = next(self.chords)
			self.currentName = next(self.chordNames)
			self._regenerateMusic()
			self.currentNote = 1

		if self.verbose:
			print "Current note="+str(self.currentNote)
			print "Current Chord="+str(self.currentName)
		self.currentNote += self.dur