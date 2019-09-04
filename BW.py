#!/usr/bin/python3

from  BWCommon import *
from BWControl import *

import wx
import sys
import getopt
import os
import ctypes
import wx.py as py

os = 'linux'
if sys.platform.startswith("win"):
    os = 'win'

def main():
    app = wx.App(False)
    control = BWControl()
    app.MainLoop()

if __name__ == '__main__':
    main()

