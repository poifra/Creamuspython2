from Sequencer import Sequence, Note
from itertools import cycle
from Synth import BaseSynth, ClassicSynth, BassWalkSynth
from pyo import *
from Chordbook import durations, changeOctave

class AudioPlayer():
	def __init__(self, tempo, chords, chordNames, verbose = True):
		self.serv = Server().boot()
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.currentNote = 1
		self.noteCounter = Pattern(self._timer,self.dur)
		self.setChords(chords, firstTime = True, cNames = chordNames)
		self.firstChord = self.currentChord
		self.totalCount = 1
		self.verbose = verbose

	def play(self, tempo):
		self.tempo = tempo
		self.dur = 60/(tempo / durations['quarter'] / 4)
		self.noteCounter.setTime(self.dur)
		self.noteCounter.play()
		self.serv.start()

	def stop(self):
		if self.bassSeq.isPlaying():
			self.bassSeq.stop()
		for seq in self.chordSeqs:
			if seq.isPlaying():
				seq.stop()

		self.currentNote = 1
		self.currentChord = self.firstChord
		self.currentBass
		self.noteCounter.stop()
		self.serv.stop()

	def setChords(self, chords, firstTime = False, cNames = None):
		print "in setChords",cNames
		self.chords = []
		self.bassNotes = []
		for c in chords:
			self.chords.append(changeOctave(c,amount=2))
			self.bassNotes.append(c)

		self.chords = cycle(self.chords)
		self.bassNotes = cycle(self.bassNotes)
		self.chordNames = cycle(cNames)

		self.currentChord = next(self.chords)
		self.currentBass = next(self.bassNotes)
		self.currentName = next(self.chordNames)
		self._regenerateMusic(firstTime)

	def _regenerateMusic(self, firstTime = False):
		newBass = [Note(n, durations['quarter']) for n in self.currentBass]
		newChord = [Note(n, durations['half']) for n in self.currentChord]
		
		if firstTime:
			self.bassSeq = Sequence(newBass, self.tempo)
			self.bassSynth = BassWalkSynth(self.bassSeq)
			self.chordSeqs = [Sequence([note],self.tempo) for note in newChord]
			self.chordSynths = [ClassicSynth(c,amp=0.1) for c in self.chordSeqs]
		else:
			if self.bassSeq.isPlaying:
				self.bassSeq.stop()
			for seq in self.chordSeqs:
				if seq.isPlaying:
					seq.stop()

			self.bassSynth.set_notes(newBass)
			self.chordSeqs = [Sequence([note],self.tempo) for note in newChord]
			self.chordSynths = [ClassicSynth(c,amp=0.1) for c in self.chordSeqs]
			
		self.bassSynth.get_out().out()
		if not(self.bassSeq.isPlaying):
			self.bassSeq.play()

		for s in self.chordSynths:
			s.get_out().out()
		for seq in self.chordSeqs:
			if not(seq.isPlaying):
				seq.play()

		# self.bassSeq.play()
		# self.bassSynth = BassWalkSynth(self.bassSeq)
		# self.bassSynth.get_out().out()

		# self.chordSeqs = [Sequence([note],self.tempo) for note in newChord]

		# for seq in chordSeqs:
		# 	seq.play()
		# self.chordSynths = [ClassicSynth(c,amp=0.1) for c in chordSeqs]
		# for s in self.chordSynths:
		# 	s.get_out().out()

	def _timer(self):
		if self.currentNote > 4:
			self.currentChord = next(self.chords)
			self.currentName = next(self.chordNames)
			self._regenerateMusic()
			self.currentNote = 1

		if self.verbose:
			print "Current note="+str(self.currentNote)+" Total count="+str(self.totalCount)
			print "Current Chord="+str(self.currentName)
		self.currentNote += self.dur
		self.totalCount += 1