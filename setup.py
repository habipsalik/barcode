import cx_Freeze
import sys

company_name = 'B-OSS Reader'
product_name = 'B-OSS'

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    }

build_exe_options = {
    "packages":["Tkinter", "pyzbar", "numpy"],
    "include_files":["C:/User/barcode/b-oss.ico"],
    }

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("C:/User/barcode/main.py", base=base, icon="C:/User/barcode/b-oss.ico")]

cx_Freeze.setup(
    name = "B-OSS",
    options = {'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options},
    version = "1.0",
    description = "Reader application",
    executables = executables
    )