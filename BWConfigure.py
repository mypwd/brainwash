
import os.path
import json
from BWMisc import *
DEFAULT_CONF_FILE='_conf.json'
DEFAULT_DB_FILE='db/default.db'


class BWConfigure:
    def __init__(self, conffile = ''):
        self.conf = None
        _conffile = None
        
        if len(conffile) == 0:
            _conffile = DEFAULT_CONF_FILE
        else :
            _conffile = conffile
            
        if os.path.exists(_conffile) == False:
            print('Error : Configuration load fail\n')
            exit(2)
        else:
            if self.load_config(_conffile) < 0 :
                print('Error : Configuration load fail\n')
                exit(2)
        self.conffile = _conffile
    def set_used_db(self, db):
        self.conf['db'] = db
    def get_used_db(self):
        if os.access(self.conf['db'], os.F_OK) :
            return self.conf['db']
        return None
    def load_config(self, path):
        raw = ''
        res = -1
        with open(path) as f:
            raw = f.read()
        
            try:
                self.conf = json.loads(raw)
                res = 0
            except:
                res = -1
        if not 'db' in self.conf:
            self.conf['db'] = DEFAULT_DB_FILE
            
        print(self.conf['db'])
        
        if res == -1:
            return -1
        else:
            return 0
        
    def save(self):
        BWMisc().save_json_file(self.conffile, self.conf)
        
