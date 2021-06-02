import wx
import wx.lib.scrolledpanel as scrolled

text = '''
ScrolledPanel extends wx.ScrolledWindow, adding all
the necessary bits to set up scroll handling for you.

Here are three fixed size examples of its use. The
demo panel for this sample is also using it -- the
wx.StaticLine below is intentionally made too long so a scrollbar will be
activated.'''

class TestPanel(scrolled.ScrolledPanel):

    def __init__(self, parent):

        scrolled.ScrolledPanel.__init__(self, parent, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)

        desc = wx.StaticText(self, -1, text)

        desc.SetForegroundColour("Blue")
        vbox.Add(desc, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(wx.StaticLine(self, -1, size=(1024, -1)), 0, wx.ALL, 5)
        vbox.Add((20, 20))

        self.SetSizer(vbox)
        self.SetupScrolling()


app = wx.App(0)
frame = wx.Frame(None, wx.ID_ANY)
fa = TestPanel(frame)
frame.Show()
app.MainLoop()
"""
        self.text_3 = wx.StaticText(self, wx.ID_ANY, "Text3", size = (-1, 50))
        self.text_4 = wx.StaticText(self, wx.ID_ANY, "Text4", size = (-1, 50))
        self.text_5 = wx.StaticText(self, wx.ID_ANY, "Text5", size = (-1, 50))
        self.text_6 = wx.StaticText(self, wx.ID_ANY, "Text6", size = (-1, 50))
        self.text_7 = wx.StaticText(self, wx.ID_ANY, "Text7", size = (-1, 50))
        self.text_8 = wx.StaticText(self, wx.ID_ANY, "Text8", size = (-1, 50))
        self.text_9 = wx.StaticText(self, wx.ID_ANY, "Text9", size = (-1, 50))
        self.text_10 = wx.StaticText(self, wx.ID_ANY, "Text10", size = (-1, 50))
        self.text_11 = wx.StaticText(self, wx.ID_ANY, "Text11", size = (-1, 50))
        self.text_12 = wx.StaticText(self, wx.ID_ANY, "Text12", size = (-1, 50))

                self.sizer.Add(self.text_3, 0, wx.ALL, 0)
        self.sizer.Add(self.text_4, 0, wx.ALL, 0)
        self.sizer.Add(self.text_5, 0, wx.ALL, 0)
        self.sizer.Add(self.text_6, 0, wx.ALL, 0)
        self.sizer.Add(self.text_7, 0, wx.ALL, 0)
        self.sizer.Add(self.text_8, 0, wx.ALL, 0)
        self.sizer.Add(self.text_9, 0, wx.ALL, 0)
        self.sizer.Add(self.text_10, 0, wx.ALL, 0)
        self.sizer.Add(self.text_11, 0, wx.ALL, 0)
        self.sizer.Add(self.text_12, 0, wx.ALL, 0)"""