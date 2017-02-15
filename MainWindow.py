import wx

class MainWindow(wx.Frame):
	def __init__(self,title="Chords PogChamp", 
			size=wx.DefaultSize, pos=wx.DefaultPosition):
		wx.Frame.__init__(self,None,title=title,pos=pos,size=size)
		self.panel = wx.Panel(self, wx.ID_ANY)
		self.Show()


app = wx.App()
f = MainWindow(size=(400,400))
app.MainLoop()