# coding:utf-8
from __future__ import division
from Chordbook import durations
from pyo import midiToHz, Metro, Iter, Ceil

class Sequence:
	def __init__(self, notes=[], tempo=80):
		self.notes = [note.frequency for note in notes]
		self.times = [note.time(tempo) for note in notes]
		self.amps = [note.amp for note in notes]
		self.tempo = tempo
		self._metro = Metro()
		self.amp = Iter(self._metro, self.amps, init=self.amps[0])
		self.time = Iter(self._metro, self.times, init=self.times[0])
		self._metro.setTime(self.time)
		self.signal = Iter(self._metro, self.notes)
		#triggers are only sent when amp is >0
		self.trigger = Ceil(self.amp*self._metro)
		self.playing = False

	def append(self, note):
		self.notes.append(note.frequency)
		self.rythms.append(note.time(tempo))
		self.amps.append(note.amp)

		self.amp.setChoice(self.amps)
		self.time.setChoice(self.times)
		self.signal.setChoice(self.notes)

	def set_notes(self, notes):
		self.notes = [note.frequency for note in notes]
		self.rythms = [note.time(self.tempo) for note in notes]
		self.amps = [note.amp for note in notes]

		self.amp.setChoice(self.amps)
		self.time.setChoice(self.times)
		self.signal.setChoice(self.notes)

	def play(self):
		self._metro.play()
		self.playing = True
		return self

	def isPlaying(self):
		return self.playing

	def stop(self):
		self.playing = False
		self._metro.stop()

class Note:
	def __init__(self, note, duration, amp=1):
		self.note = note
		self.duration = duration
		self.amp = amp
		self.frequency = midiToHz(self.note)

	def time(self, tempo=80):
		return 60/(tempo / self.duration / 4)

	def __repr__(self):
		return "Note="+str(self.note)+" duration="+str(self.duration)+" Freq="+str(self.frequency)