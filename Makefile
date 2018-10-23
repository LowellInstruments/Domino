# Adapted from various Makefiles from projects under
# https://github.com/masschallenge.
# All aspects that are copyrighted by MassChallenge or Nathan Wilson
# are available under the MIT License.


.PHONY: help code-check coverage dist run test


help:
	@echo Valid targets are:
	@echo help - Prints this help message
	@echo code-check - Runs pycodestyle on all python code in the project
	@echo coverage - Use pytest to run all tests and report on test coverage
	@echo dist - Creates a single executable package for the local OS
	@echo run - Runs coverter application
	@echo test - Use pytest to run all tests


VENV = venv

ALL_FILES := $(wildcard *.py */*.py)
EXCLUDE_FILES := $(wildcard */*_ui.py */*_rc.py) \
  converter/progress.py \
  converter/options.py

CHECK_FILES := $(filter-out $(EXCLUDE_FILES),$(ALL_FILES))

ifeq ($(OS),Windows_NT)
  CP = copy
  GIT_HOOKS_TARGET = .git\hooks\pre-commit
  GIT_HOOKS_SOURCE = git-hooks\pre-commit
  PYTHON = python
  ACTIVATE = $(VENV)\Scripts\activate && set PYTHONPATH=.
  RMDIR_CMD := rmdir /s /q
  virtualenv = $(shell where virtualenv.exe)
  SEPARATOR = ;
else
  CP = cp
  GIT_HOOKS_TARGET = .git/hooks/pre-commit
  GIT_HOOKS_SOURCE = git-hooks/pre-commit
  PYTHON = python3
  VENV_PYTHON = -p $(PYTHON)
  ACTIVATE = export PYTHONPATH=.; . $(VENV)/bin/activate
  RMDIR_CMD = rm -rf
  virtualenv = $(shell which virtualenv)
  SEPARATOR = :
endif

tmp:
	echo $(CHECK_FILES)

DATA_DIR = "converter/Calibration Tables$(SEPARATOR)Calibration Tables"


$(GIT_HOOKS_TARGET): $(GIT_HOOKS_SOURCE)
	@$(CP) $(GIT_HOOKS_SOURCE) $(GIT_HOOKS_TARGET)


ifeq ($(virtualenv),)
  NEED_VIRTUALENV = virtualenv
endif

virtualenv:
	@pip install virtualenv


$(VENV): $(NEED_VIRTUALENV) requirements.txt $(GIT_HOOKS_TARGET)
	@-$(RMDIR_CMD) $(VENV)
	@virtualenv $(VENV_PYTHON) $@
	@$(ACTIVATE) && pip install -r requirements.txt


code-check: $(VENV)
	@$(ACTIVATE) && flake8 $(CHECK_FILES)


run: $(VENV)
	@$(ACTIVATE) && $(PYTHON) -m gui.main


test: $(VENV)
	@$(ACTIVATE) && pytest


coverage: $(VENV)
	@$(ACTIVATE) && pytest --cov=setup_file --cov-report=term \
	  --cov-report=html


dist: $(VENV)
	@-$(RMDIR_CMD) dist
	@$(ACTIVATE) && pyinstaller converter/main.py \
	  --add-data $(DATA_DIR) \
	  --onefile --noconsole
