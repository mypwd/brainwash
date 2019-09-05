import wx

from wx.lib.splitter import MultiSplitterWindow
import wx.py as py
from pubsub import pub
import os
import wx.dataview as dv
import sys

BATCH_OPEN_ID=2001
BATCH_SAVE_ID=2002
BATCH_NEW_ID=2003

class DisplayCommon:
    def __init__(self):
        pass
    def wrap_horizontal_sizer(self, lst):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for l in lst:
            sizer.Add(l, 1, wx.LEFT | wx.RIGHT |wx.ALIGN_CENTER_VERTICAL, 5)
        return sizer
    def wrap_vertical_sizer(self, lst):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for l in lst:
            sizer.Add(l, 1)
        return sizer
    def errormsg(self, msg):
        dlg = wx.MessageDialog(self, msg,
                               'BrainWash',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()


class BWNoteList(wx.Panel, DisplayCommon):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   | dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   )


        self.dvc.AppendTextColumn('id', 0, width=100)
        self.dvc.AppendTextColumn('question', 1, width=300)
        self.dvc.AppendTextColumn('level', 2, width=100)
        self.dvc.AppendTextColumn('date', 3, width=100)

        
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True
        self.dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.onSelect)

        self.add_btn = wx.Button(self, wx.ID_ANY, "새글")
        self.rm_btn = wx.Button(self, wx.ID_ANY, "제거")
        self.mod_btn = wx.Button(self, wx.ID_ANY, "수정")
        s = self.wrap_horizontal_sizer([self.add_btn, self.rm_btn, self.mod_btn])
        self.add_btn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.rm_btn.Bind(wx.EVT_BUTTON, self.onRemove)
        self.mod_btn.Bind(wx.EVT_BUTTON, self.onModify)
        self.rm_btn.Enable(False)
        self.mod_btn.Enable(False)
        
        question_box = wx.StaticBoxSizer(wx.VERTICAL, self, "Question")
        self.question_tb = wx.TextCtrl(self, -1, size=(600, 60), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP)
        self.question_tb.SetBackgroundColour(wx.LIGHT_GREY)
        question_box.Add(self.question_tb, 10, wx.LEFT|wx.RIGHT | wx.EXPAND, 5)
        
        solution_box = wx.StaticBoxSizer(wx.VERTICAL, self, "Solution")
        self.solution_tb = wx.TextCtrl(self, -1, size=(600, 60), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP)
        self.solution_tb.SetBackgroundColour(wx.LIGHT_GREY)
        solution_box.Add(self.solution_tb, 10, wx.LEFT|wx.RIGHT | wx.EXPAND, 5)
        self.level_cb = wx.ComboBox(self, id=wx.ID_ANY, style=wx.CB_DROPDOWN, size=(200,30))
        for i in range(1,11):
            self.level_cb.Append('Level{}'.format(i), i)
        self.level_cb.SetSelection(0)

        self.submit_btn = wx.Button(self, wx.ID_ANY, "추가")
        self.submit_btn.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.submit_btn.Enable(False)
        l = self.wrap_horizontal_sizer([self.level_cb, self.submit_btn])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.dvc, 10, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND )
        sizer.Add(s, 1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND)
        sizer.Add(question_box, 1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND)
        sizer.Add(solution_box, 1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND)
        sizer.Add(l, 1, wx.CENTRE | wx.TOP|wx.BOTTOM, 5 )
        self.SetSizer(sizer)

    def initialize(self):
        pass
        
    def thread_stop(self):
        pass
    def set_model(self, model):
        self.dvc.AssociateModel(model)
    def set_question(self, data):
        self.question_tb.SetBackgroundColour(wx.Colour(0xeb, 0xee, 0xd0))
        self.solution_tb.SetBackgroundColour(wx.Colour(0xeb, 0xee, 0xd0))

        self.question_tb.Clear()
        self.question_tb.SetValue(data[2])
        self.solution_tb.Clear()
        self.solution_tb.SetValue(data[3])
        self.level_cb.SetSelection(data[4])

        self.submit_btn.Enable(False)
        self.mod_btn.Enable(True)
        self.rm_btn.Enable(True)
    def onAdd(self, evt):
        self.question_tb.Clear()
        self.question_tb.SetBackgroundColour(wx.Colour(0xc3, 0xed, 0xba))
        self.solution_tb.Clear()
        self.solution_tb.SetBackgroundColour(wx.Colour(0xc3, 0xed, 0xba))

        self.submit_btn.Enable(True)
        self.mod_btn.Enable(False)
        self.rm_btn.Enable(False)
        
    def onModify(self, evt):
        print('mod')
    def onRemove(self, evt):
        print('rem')
    def onSubmit(self, evt):
        q = self.question_tb.GetValue()
        s = self.solution_tb.GetValue()
        l = self.level_cb.GetSelection()
        print(q,s,l)
        if len(q) < 4 or len(s) < 4:
            self.errormsg('4글자 이상 채워주세요')
            return
        pub.sendMessage('add_question', question=q, solution=s, level = l)
    def onSelect(self, evt):
        try:
            item = evt.GetItem()
            model = self.dvc.GetModel()
            row = model.GetRow(item)
            print('row', row)
            pub.sendMessage('question_selected', row=row)
        except:
            pass
        
        
class BWNoteTraining(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(sizer)

    def initialize(self):
        pass
        
    def thread_stop(self):
        pass

class BWNoteTest(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(sizer)

    def initialize(self):
        pass
        
    def thread_stop(self):
        pass

class BWNoteResult(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(sizer)

    def initialize(self):
        pass
        
    def thread_stop(self):
        pass


class BWDisplay(wx.Frame, DisplayCommon):
  
    def __init__(self):
        wx.Frame.__init__(self, None, 1001, 'Brain Wash',
                          size=(700, 700))
        self.initialize()
        self.Centre()
        self.Layout()
        self.Show()
        
    def initialize(self):
        p = wx.Panel(self, style = wx.BORDER_NONE)
        self.main_sizer = wx.BoxSizer()
        self.init_toolbar()

        menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        menu1.Append(101, "&About", "")
        menuBar.Append(menu1, "About")
        self.SetMenuBar(menuBar)
        if sys.platform.startswith("win"):
            self.init_note(p)
        else:
            self.init_note(self)

        #sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.main_sizer)
    def init_toolbar(self):
        self.tb = self.CreateToolBar()
        tsize = (24,24)
        #new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        #save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        self.tb.SetToolBitmapSize(tsize)
        self.tb.AddTool(BATCH_NEW_ID, "Create DB", new_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Create DB")
        self.tb.AddTool(BATCH_OPEN_ID, "Open DB", open_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Open DB")
        #self.tb.AddTool(BATCH_SAVE_ID, "Save DB", save_bmp, wx.NullBitmap, wx.ITEM_NORMAL, "Save DB")

        self.tb.EnableTool(BATCH_SAVE_ID, False)
        self.tb.SetToolBitmapSize(tsize)
        self.tb.Realize()
        self.Bind(wx.EVT_TOOL, self.onToolClick)
    def init_note(self, parent):
        #p = wx.Panel(parent)
        print(parent)
        self.nb = wx.Notebook(parent)
        

        self.nb_list = BWNoteList(self.nb)
        self.nb.AddPage(self.nb_list, 'List')
        
        self.nb_training = BWNoteTraining(self.nb)
        self.nb.AddPage(self.nb_training, 'Training')

        self.nb_test = BWNoteTest(self.nb)
        self.nb.AddPage(self.nb_test, 'Test')

        self.nb_result = BWNoteResult(self.nb)
        self.nb.AddPage(self.nb_result, 'Result')
        
        self.main_sizer.Add(self.nb, 1, wx.EXPAND | wx.ALL , 5)

    def onToolClick(self, evt):
        id = evt.GetId()
        if id == BATCH_NEW_ID :
            print('new')
            self.new_db()
        elif id == BATCH_OPEN_ID:
            print('open')
            self.open_db()
        
    def new_db(self):
        db_name = ''
        dlg = wx.TextEntryDialog(
            self, 'DB 이름을 입력하세요',
                'DB 생성')

        dlg.SetValue("default")

        if dlg.ShowModal() == wx.ID_OK:
            db_name = dlg.GetValue()

        dlg.Destroy()
        pub.sendMessage('new_db', db=db_name)
    def open_db(self):
        path = ''
        wildcard = "BrainWash (*.db)|*.db|" \
           "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd() + '/db',
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | 
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
        dlg.Destroy()
        if len(path):
            pub.sendMessage('open_db', db=path)

    def set_model(self, model):
        self.nb_list.set_model(model)

    def set_question(self, data):
        self.nb_list.set_question(data)
