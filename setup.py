#!/usr/bin/python3

from cx_Freeze import setup, Executable
base = "Win32GUI"
executable = [
    Executable("BW.py", base=base),
]

include_module = []
exclude_module = []

include_file = [
    '_conf.json'
    ]
setup(name = "test" ,
      version = "0.1" ,
      description = "" ,
      executables = executable,
      options = {"build_exe":
                 { "include_files":include_file ,
                   "includes":include_module,
                   "packages":["os", "idna", "dbm"]}
                 
      }
)
