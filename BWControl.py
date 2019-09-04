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

    def subscribe_all(self):
        """
        pub.subscribe(self.do_debug, 'debug')
        """
        pass
