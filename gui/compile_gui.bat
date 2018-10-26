call ../venv/Scripts/activate.bat
@echo on
pyuic5 designer_files/container.ui -o container_ui.py -x --from-imports
pyuic5 designer_files/converter.ui -o converter_ui.py -x --from-imports
pyuic5 designer_files/setup.ui -o setup_ui.py -x --from-imports
pyuic5 designer_files/start_stop.ui -o start_stop_ui.py -x --from-imports
pyuic5 designer_files/progress.ui -o progress_ui.py -x --from-imports
pyuic5 designer_files/options.ui -o options_ui.py -x --from-imports
pyrcc5 designer_files/icons.qrc -o icons_rc.py
call ../venv/Scripts/deactivate.bat