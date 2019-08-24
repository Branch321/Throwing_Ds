# set up file for cx_freeze
# you need to run python setup.py bidst_msi to generate the executable

import sys
from cx_Freeze import setup, Executable
includesfiles = {"include_files": ['updater_settings.ini']}
base = None
if sys.platform == "win32":
    base = "Console"

setup(  name = "Ice Era Assistant",
        version = "1.0",
        options = {'build_exe': includesfiles},
        description = "Ice Era Assistant",
        executables = [Executable("updater.py", base=base)])