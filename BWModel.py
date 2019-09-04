import wx
import wx.dataview as dv
import operator
from pubsub import pub
import sqlite3
import os, re
import time
        
class BWModel(dv.DataViewIndexListModel):
    def __init__(self):
        self.data = []
        dv.DataViewIndexListModel.__init__(self, len(self.data))
        self.db = None
        self.db_conn = None
        self.db_curr = None
    def AddRow(self, value):
        self.data.append(value)
        self.RowAppended()

    def GetColumnType(self, col):
        return "string"

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        return self.data[row][col]

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        self.data[row][col] = value
        return True

    # TODO 데이터 입력전에는 알 수 없음
    def GetColumnCount(self):
        return 3

    # 
    def GetCount(self):
        return len(self.data)
    # TODO
    def GetAttrByRow(self, row, col, attr):
        return False

    # TODO
    def op_cmp(self, i1, i2):
        if operator.eq(i1,i2):
            return 0
        if operator.lt(i1,i2):
            return -1
        else:
            return 1
    def Compare(self, item1, item2, col, ascending):
        
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0 :
            return self.op_cmp(int(self.data[row1][col]), int(self.data[row2][col]))
        else:
            return self.op_cmp(self.data[row1][col], self.data[row2][col])
        


    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)

        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)

    def data_clear(self):
        rows = []
        for i in range(0,len(self.data)):
            rows.append(i)
            
        wx.CallAfter(self.DeleteRows, rows)
        
    def create_db(self, db_name):
        if not self.db_conn == None:
            self.db_conn.close()
            self.db_conn = None
            self.data_clear()
        self.db = 'db/'+db_name+'.db'

        if os.access(self.db, os.F_OK) :
            return -1                     # file exists
        try:
            query = "create table  if not exists question(idx integer primary key autoincrement, ts int, question text, level int)"
            self.db_conn = sqlite3.connect(self.db, check_same_thread=False)
            self.db_curr = self.db_conn.cursor()
            self.db_curr.execute(query)
            query = "create table if not exists solution(idx  integer primary key autoincrement, ts int, solution text, question_id int)"
            self.db_curr.execute(query)
            query = "create table if not exists test(idx  integer primary key autoincrement, ts int, level int, subject text)"
            self.db_curr.execute(query)
            query = "create table if not exists answer(idx  integer primary key autoincrement, ts int, answer text, question_ids int, test_idx int, result int)"
            self.db_curr.execute(query)
            self.db_conn.commit()
        except:
            return -2                     # db fail

        return 0
    def open_db(self, db_name):
        
        if not os.access(db_name, os.F_OK) :
            return -1                     # file not exists
        if not self.db_conn == None:
            self.db_conn.close()
            self.db_conn = None
            self.data_clear()
        self.db = db_name    
        self.db_conn = sqlite3.connect(self.db, check_same_thread=False)
        self.db_curr = self.db_conn.cursor()
        
        return 0
    def add_question(self, q, s, l):
        ts = time.time()
        
        self.db_curr.execute("insert into question (ts, question, level) values (?, ?, ?)",(ts, q, l))
        qidx = self.db_curr.lastrowid
        self.db_curr.execute("insert into solution (ts, solution, question_id) values (?, ?, ?)",(ts, s, qidx))
        self.db_conn.commit()
    
        
