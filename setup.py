import sys
import cx_Freeze
import distutils
import opcode
import os

product_name = 'B-OSS Reader'
distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')

build_exe_options = {
    "packages":["Tkinter", "pyzbar", "numpy", "pylibdmtx"],
    "include_files":[(distutils_path, 'lib/distutils'), ".\\data"],
    "excludes": ["distutils"]
    }

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name = "B-OSS",
    options = {'build_exe': build_exe_options},
    version = "1.0.1",
    description = "Reader application",
    executables = executables,
    )