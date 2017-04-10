from Sequencer import Sequence, Note
from itertools import cycle
from Synth import BaseSynth, ClassicSynth

class AudioPlayer():
	def __init__(self, tempo, chords):
		self.tempo = tempo
		self.currentBar = chords[0]
		self.currentNote = 0
		self.bassSynth = BassWalkSynth()
		self.chordSynth = ClassicSynth()
		self.chords = cycle(chords)
		self.noteCounter = Pattern(_timer,duration)

	def getPlayer(self, playerType):
		seq = Sequence(self.notes,tempo=90)
		syn = playerType(seq)
		return syn

	def _regenerateMusic(self):
		pass

	def _timer(self):
		self.currentNote += duration
		if self.currentNote > 4:
			self.currentBar = next(self.chords)
			self._regenerateMusic()
			self.currentNote = 0