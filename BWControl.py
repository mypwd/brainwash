from BWDisplay import *
from BWCommon import *
from BWModel import *
from BWConfigure import *
from pubsub import pub
from pubsub.utils.notification import useNotifyByWriteFile

class BWControl:
    def __init__(self):
        
        self.configure = BWConfigure()
        self.subscribe_all()        
        self.display = BWDisplay()
        self.model = BWModel()
        self.display.set_model(self.model)
        db = self.configure.get_used_db()
        if db != None:
            self.do_open_db(db)
        self.display.initialize()
    def subscribe_all(self):
        """
        pub.subscribe(self.do_debug, 'debug')
        """
        pub.subscribe(self.do_new_db, 'new_db')
        pub.subscribe(self.do_open_db, 'open_db')
        pub.subscribe(self.do_add_question, 'add_question')
        pub.subscribe(self.do_mod_question, 'mod_question')
        pub.subscribe(self.do_del_question, 'del_question')
        pub.subscribe(self.do_question_seletected, 'question_selected')
        pub.subscribe(self.do_filter_changed, 'filter_changed')
        pub.subscribe(self.do_training_next, 'training_next')
        pub.subscribe(self.do_training_confirm, 'training_confirm')
        
    def do_new_db(self, db):
        ret = self.model.create_db(db)
        if ret == -1:
            wx.CallAfter( self.display.errormsg, msg = 'File Exists')
        elif ret == -2:
            wx.CallAfter( self.display.errormsg, msg = 'DB Error')
        elif ret == 0:
            self.configure.set_used_db(db)
    def do_open_db(self, db):
        print(db)
        ret = self.model.open_db(db)
        if ret == 0 :
            self.model.load_db()
            self.configure.set_used_db(db)

    def do_add_question(self, question, solution, level):
        ret = self.model.add_question(question, solution, level)
        if ret < 0 :
            wx.CallAfter( self.display.errormsg, msg = 'DB Error')
            return

    def do_mod_question(self, row, question, solution, level):
        ret = self.model.mod_question(row, question, solution, level)
        if ret < 0 :
            wx.CallAfter( self.display.errormsg, msg = 'DB Error')
            return

    def do_del_question(self, row):
        ret = self.model.del_question(row)
        if ret < 0 :
            wx.CallAfter( self.display.errormsg, msg = 'DB Error')
            return
        
    def do_question_seletected(self, row):
        print('do')
        ret = self.model.get_question_by_row(row)
        print('ret', ret)
        if not ret == None:
            print('ret')
            wx.CallAfter( self.display.set_question, data = ret)

    def do_filter_changed(self, under, level):
        self.model.filter_changed(under, level)
        count = self.model.get_filtered_count()
        wx.CallAfter(self.display.nb_training.update_counter, count)

    def do_training_next(self):
        idx, q = self.model.get_training_next()
        if idx < 0:
            wx.CallAfter( self.display.errormsg, msg = '질문이 없습니다.' )
        else:
            wx.CallAfter(self.display.nb_training.update_question, idx, q)
        
    def do_training_confirm(self, idx, answer):
        solution, answer, score, match = self.model.get_training_solution(idx, answer)
        wx.CallAfter(self.display.nb_training.update_result, solution, answer, score, match)
