## Run this file to convert the MatToDicom.py file to standalone executable
## See pyinstaller documentation for more information
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py', # compile the program
    '--onefile', # Produce a standalone exe
    '--icon=Comp_Brain.ico', # icon in file exploer
    '--additional-hooks-dir=.', # dir containing files that specify extra hooks
    '--noconsole' # Do not show the command prompt when executing
])