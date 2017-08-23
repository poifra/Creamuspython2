import wx
import MyRandoms as mr

class OptionWindow(wx.Frame):
	def __init__(self, parent=None, id=-1, title='Preferences'):
		wx.Frame.__init__(self, parent, id, title, (-1, -1), wx.Size(450, 400))
		self.options = Options()
		self.Centre()

class Options():
	def __init__(self):
		self.options = {
			"algo" : "loopseg",
			"x1" : 1,
			"x2" : 0.3
		}

	def setValue(self, key):
		self.options[key] = value

	def getValue(self,key):
		return self.options[key]