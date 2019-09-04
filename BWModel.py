import wx
import wx.dataview as dv
import operator
from pubsub import pub


        
class BWModel(dv.DataViewIndexListModel):
    def __init__(self):
        self.data = []
        dv.DataViewIndexListModel.__init__(self, len(self.data))

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

        
