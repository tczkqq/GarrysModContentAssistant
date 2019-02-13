import os
os.environ['TCL_LIBRARY'] = "C:\\Program Files (x86)\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Program Files (x86)\\Python36-32\\tcl\\tk8.6"
from cx_Freeze import setup, Executable

buildOptions = dict(
    packages = [],
    excludes = [],
    include_files=['c:/Program Files (x86)/Python36-32/DLLs/tcl86t.dll', 'c:/Program Files (x86)/Python36-32/DLLs/tk86t.dll',('resources/icon.ico','resources/icon.ico'),('resources/header.png','resources/header.png'),'links.ini']
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Garry\'s Mod Content Assistant.py', base=base,icon="resources/icon.ico")
]

setup(name='Garry\'s Mod Content Assistant',
      version = '0.2',
      description = 'Garry\'s Mod Content Assistant',
	  author_email='jarnutek@gmail.com',
	  url='https://gamebanana.com/tools/6292',
      author="Tomeczekqq",
      options = dict(build_exe = buildOptions),
      executables = executables
      )
