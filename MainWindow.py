#encoding:utf-8
import wx
from Chordbook import chords, chordSymbols, shiftFactors

class CustomFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(450, 330), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

		self.chords = ['Dm7','G7','C7'] #initial progression
		self.panel = wx.Panel(self, -1)

		self.btnAdd = wx.Button(self.panel, -1, 'Ajouter accord')
		self.btnAdd.Bind(wx.EVT_BUTTON, self.onAddChord)

		self.btnRemove = wx.Button(self.panel, -1, 'Supprimer accord')
		self.btnRemove.Bind(wx.EVT_BUTTON, self.onDeleteChord)
		
		self.btnPlay = wx.Button(self.panel, -1, 'PLAY')
		self.btnPlay.Bind(wx.EVT_BUTTON, self.onPlay)

		self.btnStop = wx.Button(self.panel, -1, 'STOP')
		self.btnStop.Bind(wx.EVT_BUTTON, self.onStop)

		self.chordLabel = wx.StaticText(self.panel, id=-1, label=" -- ".join(self.chords), pos=(-1,-1), size=(-1,-1), 
			style=wx.ALIGN_CENTRE_HORIZONTAL)

		self.chordKeys = wx.ListBox(self.panel, -1, pos=wx.Point(8, 48), size=wx.Size(75, 256), 
			choices = sorted(shiftFactors.keys()), style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)
		self.chordQualities = wx.ListBox(self.panel, -1, pos=wx.Point(32, 64),size=wx.Size(184, 256),
			choices = sorted(chords.keys()), style = wx.LB_SINGLE | wx.LB_ALWAYS_SB)
		
		self.containerSizer = wx.BoxSizer(wx.VERTICAL)
		self.chordChooserSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnAddRemoveSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btnPlayStopSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.displaySizer = wx.BoxSizer(wx.HORIZONTAL)

		self.btnAddRemoveSizer.Add(self.btnAdd, 1, wx.EXPAND)
		self.btnAddRemoveSizer.Add(self.btnRemove, 1, wx.EXPAND)

		self.btnPlayStopSizer.Add(self.btnPlay, 1, wx.EXPAND)
		self.btnPlayStopSizer.Add(self.btnStop, 1, wx.EXPAND)

		self.chordChooserSizer.Add(self.chordKeys, 1, wx.EXPAND)
		self.chordChooserSizer.Add(self.chordQualities, 1, wx.EXPAND)

		self.displaySizer.Add(self.chordLabel, 1 , wx.EXPAND)

		self.containerSizer.Add(self.chordChooserSizer, 0, wx.EXPAND)
		self.containerSizer.Add(self.btnAddRemoveSizer, 0, wx.EXPAND)
		self.containerSizer.Add(self.displaySizer, 0, wx.ALIGN_CENTER)
		self.containerSizer.Add(self.btnPlayStopSizer, 0, wx.EXPAND)
		
		self.panel.SetSizer(self.containerSizer)
		self.Centre()
	
	def _updateLabel(self):
		self.chordLabel.SetLabel(" -- ".join(self.chords))
		self.displaySizer.Layout()
		self.containerSizer.Layout()

	def onAddChord(self, event):
		#stack based logic, will change in the future
		if self.chordQualities.GetSelection() == -1 or self.chordKeys.GetSelection() == -1:
			print "YOU MUST CHOOSE ADDITIONAL DATA"
			return

		key = self.chordKeys.GetString(self.chordKeys.GetSelection())
		quality = self.chordQualities.GetString(self.chordQualities.GetSelection())
		symbol = chordSymbols[quality]
		print "Adding "+key+symbol
		self.chords.append(key+symbol)
		print self.chords
		self._updateLabel()

	def onDeleteChord(self, event):
		#stack based logic, will change in the future
		self.chords.pop()
		self._updateLabel()

	def onPlay(self, event):
		print("TWADO PLAY")

	def onStop(self, event):
		print("TWADO STOP")

	def getChords(self):
		return self.chordProg

	def setChords(self, chord, i = -1):
		if i < 0:
			self.chords.append(chord)
		else:
			self.chords.insert(i, chord)

class ChordManager(wx.App):
	def OnInit(self):
		frame = CustomFrame(None, -1, 'Super Chord Manager 3000')
		frame.Show(True)
		return True


app = ChordManager(0)
app.MainLoop()