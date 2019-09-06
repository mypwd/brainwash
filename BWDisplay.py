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

    def background_green(self, tc, start, end):
        print('start', start)
        print('end', end)
        
        tc.SetStyle(start, end, wx.TextAttr(wx.NullColour, wx.Colour(0xdc, 0xf3, 0xc2)))
        
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
        item = self.dvc.GetSelection()
        model = self.dvc.GetModel()
        row = model.GetRow(item)
        q = self.question_tb.GetValue().strip()
        s = self.solution_tb.GetValue().strip()
        l = self.level_cb.GetSelection()
        pub.sendMessage('mod_question', row = row, question = q, solution = s, level = l)
    def onRemove(self, evt):
        item = self.dvc.GetSelection()
        model = self.dvc.GetModel()
        row = model.GetRow(item)
        pub.sendMessage('del_question', row = row)

    def onSubmit(self, evt):
        q = self.question_tb.GetValue().strip()
        s = self.solution_tb.GetValue().strip()
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
        
        
class BWNoteTraining(wx.Panel, DisplayCommon):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.curr_question_idx = None
        self.confirm_toggle = 1
        # 상단
        self.under_cb = wx.CheckBox(self, -1, "Under", style=wx.ALIGN_RIGHT)

        self.level_cb = wx.ComboBox(self, id=wx.ID_ANY, style=wx.CB_DROPDOWN, size=(200,30))
        for i in range(1,11):
            self.level_cb.Append('Level{}'.format(i), i)
        self.level_cb.SetSelection(0)
        self.total = wx.StaticText(self, id=wx.ID_ANY, label="Total : ", style=wx.ALIGN_LEFT)
        s = self.wrap_horizontal_sizer([self.under_cb, self.level_cb, self.total])

        # 상단 bind
        self.Bind(wx.EVT_COMBOBOX, self.filter_change, self.level_cb)
        self.Bind(wx.EVT_CHECKBOX, self.filter_change, self.under_cb)
        
        question_box = wx.StaticBoxSizer(wx.VERTICAL, self, "Question")
        self.id = wx.StaticText(self, id=wx.ID_ANY, label=" ", style=wx.ALIGN_LEFT)
        ifont = wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        #ifont = wx.Font(13)
        self.id.SetFont(ifont)
        
        self.question = wx.StaticText(self, id=wx.ID_ANY, label=" ", style=wx.ALIGN_LEFT)
        qfont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        #qfont = wx.Font(20)
        self.question.SetFont(qfont)
        question_box.Add(self.id, 1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND, 5)
        question_box.Add(self.question, 4, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND, 5)

        # result
        result_box = wx.StaticBoxSizer(wx.VERTICAL, self, "Result")
        self.result_tb = wx.TextCtrl(self, -1, size=(600, 60), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP | wx.TE_RICH2)
        result_box.Add(self.result_tb,1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND, 5)
        
        answer_box = wx.StaticBoxSizer(wx.VERTICAL, self, "Answer")
        self.answer_tb = wx.TextCtrl(self, -1, size=(600, 60), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_BESTWRAP)
        self.answer_tb.Enable(True)
        #self.answer_tb.SetBackgroundColour(wx.LIGHT_GREY)
        self.answer_tb.SetFocus()
        #self.answer_tb.SetBackgroundColour(wx.LIGHT_GREY)
        answer_box.Add(self.answer_tb, 10, wx.LEFT|wx.RIGHT | wx.EXPAND, 5)
        
        self.submit_btn = wx.Button(self, wx.ID_ANY, "확인")
        self.next_btn = wx.Button(self, wx.ID_ANY, "다음")
        s1 = self.wrap_horizontal_sizer([ self.submit_btn, self.next_btn ])
        self.submit_btn.Bind(wx.EVT_BUTTON, self.onConfirm)
        self.next_btn.Bind(wx.EVT_BUTTON, self.onNext)

        self.Bind(wx.EVT_TEXT_ENTER, self.onEnter, self.answer_tb)
        sizer.Add(s,  1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND, 5)        
        sizer.Add(question_box,  3, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND,5)
        sizer.Add(result_box,  3, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND,5)
        
        sizer.Add(answer_box, 3, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND,5)
        sizer.Add(s1, 1, wx.LEFT|wx.RIGHT |wx.TOP|wx.BOTTOM| wx.EXPAND,5)        
        
        self.SetSizer(sizer)


    def initialize(self):
        self.filter_change(None)
        
    def thread_stop(self):
        pass

    def filter_change(self, evt):
        under = False
        if self.under_cb.IsChecked() :
            under = True
        level = self.level_cb.GetSelection()
        pub.sendMessage('filter_changed', under = under, level = level)
    def update_counter(self, count):
        self.total.SetLabel("Total : {}".format(count))
    def update_question(self, idx, q):
        self.curr_question_idx = idx
        idt = "ID : {}".format(idx)
        self.id.SetLabel(idt)
        self.question.SetLabel(q)
        self.answer_tb.SetBackgroundColour(wx.Colour(0xc3, 0xed, 0xba))
        self.answer_tb.Enable(True)
        self.answer_tb.SetFocus()
        self.confirm_toggle = 0
    def update_result(self, solution, answer, score, match):
        self.result_tb.Clear()
        sc = score * 100
        self.result_tb.write('Score : {}\n'.format(sc))
        
        self.result_tb.write(solution+'\n')
        a_start = self.result_tb.GetInsertionPoint()
        self.result_tb.write(answer+'\n')
        a_end = self.result_tb.GetInsertionPoint()

        for block in match:
            self.background_green(self.result_tb, a_start + block[1], a_start + block[1] + block[2])
            print('1', block[1], block[2])
        #self.background_green(self.result_tb, answer_start, answer_end)
        self.confirm_toggle = 1

    def onNext(self, evt):
        self.result_tb.Clear()
        self.answer_tb.Clear()
        pub.sendMessage('training_next')
    def onConfirm(self, evt):
        ans = self.answer_tb.GetValue().strip()
        if len(ans) == 0 or self.curr_question_idx == None:
            self.errormsg('질문이 없거나 답이 불충분 합니다.')
            return
        pub.sendMessage('training_confirm', idx=self.curr_question_idx, answer = ans)
    def onEnter(self, evt):
        if self.confirm_toggle == 0:
            self.confirm_toggle = 1
            self.onConfirm(None)
        else:
            self.confirm_toggle = 0
            self.onNext(None)
            
        
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

        self.Centre()
        self.Layout()
        self.Show()
        
    def initialize(self):
        self.nb_training.initialize()
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
