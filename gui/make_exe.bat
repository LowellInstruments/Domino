call ../venv/scripts/activate.bat
pyinstaller main.py --onefile -w --icon=designer_files\icons\icon.ico --add-data "Calibration Tables";"Calibration Tables"
call ../venv/scripts/deactivate.bat