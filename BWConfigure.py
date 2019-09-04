
import os.path
import json

DEFAULT_CONF_FILE='_conf.json'
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
                
        if res == -1:
            return -1
        else:
            return 0
        
