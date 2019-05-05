# B-OSS Reader

## Windows Install

### Create Virtual Environment

```bash
# go to python directory
cd C:\Python27

# get pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# install pip
python get-pip.py

# install virtualenv
python -m pip install virtualenv

# create virtual environment
python -m virtualenv barcodeenv

# activate virtual environment
barcodeenv\Scripts\activate

# install app packages
pip install -r F:\hbp\barcode1\requirements.txt

# view packages list
pip list
```

### Build app

```bash
# use cx_Freeze
python setup.py build
```

### Create Installer

##### With cx_Freeze

```bash
# create installer with cx_Freeze
python cx_Freeze_create_ins_setup.py bdist_msi
```

##### With Inno Setup Compiler

```
  Run inno setup script >> create_installer
````