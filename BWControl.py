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

    def subscribe_all(self):
        """
        pub.subscribe(self.do_debug, 'debug')
        """
        pub.subscribe(self.do_new_db, 'new_db')
        pub.subscribe(self.do_open_db, 'open_db')
        pub.subscribe(self.do_add_question, 'add_question')
        pub.subscribe(self.do_question_seletected, 'question_selected')
        
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

        
    def do_question_seletected(self, row):
        print('do')
        ret = self.model.get_question_by_row(row)
        print('ret', ret)
        if not ret == None:
            print('ret')
            wx.CallAfter( self.display.set_question, data = ret)
