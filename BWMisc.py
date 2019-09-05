import wx
import sys
from pubsub import pub

import json
#import fcntl



class BWMisc:
    def __init__(self):
        pass
    def load_json_file(self, path):
        json_data = self.read_file(path)
        if json_data == None:
            return None
        else:
            conf_data = json.loads(json_data)
        return  conf_data
    def load_file(self, path):
        chunk = self.read_file(path)
        if chunk == None:
            return None
        else:
            return chunk

    def save_json_file(self, path, j):
    
        dump = json.dumps(j, ensure_ascii=False, indent=4)
    
        _file = open(path, mode='r+', encoding='utf-8')
    
        #fcntl.flock(_file, fcntl.LOCK_EX)
        _file.seek(0)
        _file.write(dump)
        _file.truncate()
        #fcntl.flock(_file, fcntl.LOCK_UN)
        _file.close()
    
        return
    def read_file(self,path):
        f = open(path,'r+', encoding='utf-8')
    
    
        #fcntl.flock(f, fcntl.LOCK_EX)
        b = f.read()
        #fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        return b
