import wx

class OptionWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(450, 400))
		self.Centre()

class Options():
	def __init__(self):
		self.options = {
			"algo":"loopseg",
		}

	def setValue(self, key):
		self.options[key] = value

	def getValue(self,key):
		return self.options[key]