import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base, icon="b-oss1.ico")]

cx_Freeze.setup(
    name = "B-OSS",
    options = {"build_exe": {"packages":["Tkinter", "pyzbar", "numpy"], "include_files":["b-oss1.ico"]}},
    version = "0.01",
    description = "Barcodes application",
    executables = executables
    )