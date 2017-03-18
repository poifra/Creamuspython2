import wx
from Chordbook import chords
class CustomFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(450, 300))

		self.chords = []
		self.panel = wx.Panel(self, -1)
		self.btnAdd = wx.Button(self.panel, -1, 'Ajouter')
		self.btnRemove = wx.Button(self.panel, -1, 'Supprimer')
		
		self.box = wx.BoxSizer(wx.HORIZONTAL)
		self.box.Add(self.btnAdd, 1, wx.ALL)
		
		self.box.Add(self.btnRemove, 1, wx.ALL)
		self.panel.SetSizer(self.box)
		self.Centre()
	
	def getChords(self):
		return self.chordProg

	def setChords(self, chord, i = -1):
		if i < 0:
			self.chords.append(chord)
		else:
			self.chords.insert(i, chord)

class ChordManager(wx.App):
	def OnInit(self):
		frame = CustomFrame(None, -1, 'test')
		frame.Show(True)
		return True


app = ChordManager(0)
app.MainLoop()