import wx

from wx.lib.splitter import MultiSplitterWindow
import wx.py as py

BATCH_OPEN_ID=2001
BATCH_SAVE_ID=2002
BATCH_START_ID=2003
BATCH_STOP_ID=2004

class BWDisplay(wx.Frame):
  
    def __init__(self):
        wx.Frame.__init__(self, None, 1001, 'Brain Wash',
                          size=(700, 700))
        self.initialize()
        self.Centre()
        self.Layout()
        self.Show()
        
    def initialize(self):
        self.init_toolbar()
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(sizer)
    def init_toolbar(self):
        self.tb = self.CreateToolBar()
        tsize = (24,24)
        #new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        go_bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tsize)
        stop_bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, tsize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)

        self.tb.SetToolBitmapSize(tsize)
        self.tb.AddTool(BATCH_OPEN_ID, "Open DB", open_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Open DB")
        self.tb.AddTool(BATCH_SAVE_ID, "Save DB", save_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Save DB")

        self.tb.EnableTool(BATCH_SAVE_ID, False)
        self.tb.SetToolBitmapSize(tsize)
        self.tb.Realize()
        self.Bind(wx.EVT_TOOL, self.onToolClick)
    def onToolClick(self, evt):
        pass
