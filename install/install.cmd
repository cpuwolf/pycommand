set PATH=%PATH%;C:\WinPython-32bit-2.7.10.2\python-2.7.10\python.exe

cd C:\userdata\github\pycommand\


::python.exe setup.py build
::bdist_msi


::python.exe -m PyInstaller  --windowed --icon=777.ico --onefile --clean --noconfirm ff777wingflex.py

python.exe -m PyInstaller  --version-file=file_version_info.txt --windowed --onefile --clean --noconfirm pycommand.spec

pause