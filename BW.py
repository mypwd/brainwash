#!/usr/bin/python3

from  BWCommon import *
from BWControl import *

import wx
import sys
import getopt
import os
import ctypes
import wx.py as py

osp = 'linux'
if sys.platform.startswith("win"):
    osp = 'win'

def main():
    if not os.access('db', F_OK):
        os.mkdir('db')
        
    app = wx.App(False)
    control = BWControl()
    app.MainLoop()

if __name__ == '__main__':
    main()

