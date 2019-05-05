import sys
import cx_Freeze

import distutils
import opcode
import os

product_name = 'B-OSS Reader'
distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')
TARGETDIR = r'[ProgramFilesFolder]\%s' % (product_name)

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "B-OSS",                  # Name
     "[ProgramFilesFolder]",   # Component_
     "[TARGETDIR]B-OSS.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "[TARGETDIR]b-oss1.ico",  # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "[ProgramFilesFolder]"    # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': TARGETDIR,
    'data': msi_data
    }

build_exe_options = {
    "packages":["Tkinter", "pyzbar", "numpy", "pylibdmtx"],
    "include_files":[(distutils_path, 'lib/distutils'), "b-oss1.ico"],
    "excludes": ["distutils"]
    }

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", targetName="B-OSS.exe", base=base, icon="b-oss1.ico")]

cx_Freeze.setup(
    name = "B-OSS",
    options = {'build_exe': build_exe_options, 'bdist_msi': bdist_msi_options},
    version = "1.0.1",
    description = "Reader application",
    executables = executables
    )