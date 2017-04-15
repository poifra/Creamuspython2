#encoding:utf-8
import wx
from Chordbook import chords, shiftFactors, transpose
from AudioManager import AudioPlayer

class CustomFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(450, 400))
			#style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		self.DEFAULT_TEMPO = 60
		notes = sorted(['C','C#','D','D#','Db','E','Eb','F','F#','G','G#','Gb','A','A#','Ab','B','Bb'])
		notes = ['None'] + notes
		self.chords = [u'Dm7',u'G7',u'CMaj7'] #initial progression
		self.chordNotes = [transpose(key='D', target='m7'), 
						transpose(key='G', target ='7'),
						transpose(key='C', target='maj7')]

		self.panel = wx.Panel(self, -1)

		self.btnAdd = wx.Button(self.panel, -1, 'Ajouter accord')
		self.btnAdd.Bind(wx.EVT_BUTTON, self.onAddChord)

		self.btnRemove = wx.Button(self.panel, -1, 'Supprimer accord')
		self.btnRemove.Bind(wx.EVT_BUTTON, self.onDeleteChord)
		
		self.btnPlay = wx.Button(self.panel, -1, 'PLAY')
		self.btnPlay.Bind(wx.EVT_BUTTON, self.onPlay)

		self.btnStop = wx.Button(self.panel, -1, 'STOP')
		self.btnStop.Bind(wx.EVT_BUTTON, self.onStop)
		self.btnStop.Disable()

		self.chordLabel = wx.StaticText(self.panel, id=-1, label=" -- ".join(self.chords), pos=(-1,-1), size=(-1,-1), 
			style=wx.ALIGN_CENTRE_HORIZONTAL)

		self.chordKeys = wx.ListBox(self.panel, -1, pos=wx.Point(8, 48), size=wx.Size(75, 256), 
			choices = sorted(shiftFactors.keys()), style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)

		self.chordQualities = wx.ListBox(self.panel, -1, pos=wx.Point(32, 64),size=wx.Size(184, 256),
			choices = sorted(chords.keys()), style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)

		
		self.inversion = wx.ComboBox(self.panel, size=wx.DefaultSize, choices=notes)
		self.inversion.SetSelection(0)

		self.inversionLabel = wx.StaticText(self.panel, id=-1, label="Inversion : ")

		self.tempoLabel = wx.StaticText(self.panel, id=-1, label="Tempo : ")
		self.tempoTextBox = wx.TextCtrl(self.panel)
		self.tempoTextBox.SetValue(str(self.DEFAULT_TEMPO))
		self.tempo = self.DEFAULT_TEMPO
		self.tempoTextBox.Bind(wx.EVT_CHAR, self.checkForNumber)

		self.containerSizer = wx.BoxSizer(wx.VERTICAL)
		self.chordChooserSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.inversionSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnAddRemoveSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnPlayStopSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.displaySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.tempoSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.btnAddRemoveSizer.Add(self.btnAdd, 1, wx.EXPAND)
		self.btnAddRemoveSizer.Add(self.btnRemove, 1, wx.EXPAND)

		self.btnPlayStopSizer.Add(self.btnPlay, 1, wx.EXPAND)
		self.btnPlayStopSizer.Add(self.btnStop, 1, wx.EXPAND)

		self.chordChooserSizer.Add(self.chordKeys, 1, wx.EXPAND)
		self.chordChooserSizer.Add(self.chordQualities, 1, wx.EXPAND)

		self.inversionSizer.Add(self.inversionLabel, 0, wx.LEFT | wx.ALIGN_CENTER,150)
		self.inversionSizer.Add(self.inversion, 1, wx.RIGHT,150)

		self.displaySizer.Add(self.chordLabel, 1 , wx.EXPAND)

		self.tempoSizer.Add(self.tempoLabel, 1, wx.LEFT | wx.ALIGN_CENTER, 150)
		self.tempoSizer.Add(self.tempoTextBox, 1, wx.RIGHT, 150)

		self.containerSizer.Add(self.chordChooserSizer, 0, wx.EXPAND)
		self.containerSizer.Add(self.inversionSizer, 0, wx.EXPAND)
		self.containerSizer.Add(self.btnAddRemoveSizer, 0, wx.EXPAND)
		self.containerSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
		self.containerSizer.Add(self.displaySizer, 0, wx.ALIGN_CENTER)
		self.containerSizer.Add(self.btnPlayStopSizer, 0, wx.EXPAND)
		self.containerSizer.Add(self.tempoSizer, 0, wx.EXPAND)

		self.panel.SetSizer(self.containerSizer)
		self.Centre()

		self.audio = AudioPlayer(self.tempo,self.chordNotes,self.chords)
	
	def _updateLabel(self):
		self.chordLabel.SetLabel(" -- ".join(self.chords))
		self.displaySizer.Layout()
		self.containerSizer.Layout()

	def _updateBoxes(self):
		self.inversion.SetSelection(0)
		self.chordQualities.SetSelection(-1)	
		self.chordKeys.SetSelection(-1)
		self.inversionSizer.Layout()

	def onAddChord(self, event):
		#stack based logic, will change in the future
		inv = ''
		if self.chordQualities.GetSelection() == -1 or self.chordKeys.GetSelection() == -1:
			print "YOU MUST CHOOSE ADDITIONAL DATA"
			return
		if self.inversion.GetSelection() > 0:
			inv = self.inversion.GetString(self.inversion.GetSelection())

		key = self.chordKeys.GetString(self.chordKeys.GetSelection())
		quality = self.chordQualities.GetString(self.chordQualities.GetSelection())


		if quality == 'maj':
			display = ''
		else:
			display = quality

		if inv == '':
			self.chords.append(key+display)
			self.chordNotes.append(transpose(key=key,target=quality))
		else:
			self.chords.append(key+display+'/'+inv)

		print "In main window ",self.chords
		self.audio.setChords(self.chordNotes, firstTime = False, cNames = self.chords)
		self._updateBoxes()
		self._updateLabel()

	def onDeleteChord(self, event):
		#stack based logic, will change in the future
		self.chords.pop()
		self.chordNotes.pop()
		self.audio.setChords(self.chordNotes, firstTime = False, cNames = self.chords)
		self._updateLabel()

	def onPlay(self, event):
		tempo = int(self.tempoTextBox.GetValue().strip())
		
		if tempo < 30 or tempo > 300:
			print "Tempo must be between 30 and 300 bpm"
			return
		self.tempoTextBox.Disable()
		self.btnAdd.Disable()
		self.btnRemove.Disable()
		self.btnPlay.Disable()
		self.btnStop.Enable()

		print "In main window, play",self.chords
		self.audio.setChords(self.chordNotes, firstTime = False, cNames = self.chords)
		self.audio.play(tempo)
		print("TWADO PLAY")

	def onStop(self, event):
		self.audio.stop()

		self.btnAdd.Enable()
		self.btnStop.Disable()
		self.btnPlay.Enable()
		self.btnRemove.Enable()
		self.tempoTextBox.Enable()

		print("TWADO STOP")

	def checkForNumber(self, event):
		keycode = event.GetKeyCode()
		if chr(keycode) in [str(i) for i in range(10)] or keycode == 8:
			event.Skip()

class ChordManager(wx.App):
	def OnInit(self):
		frame = CustomFrame(None, -1, 'Chord Helper')
		frame.Show(True)
		return True


app = ChordManager(0)
app.MainLoop()