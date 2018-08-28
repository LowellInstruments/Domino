# Adapted from various Makefiles from projects under
# https://github.com/masschallenge.
# All aspects that are copyrighted by MassChallenge or Nathan Wilson
# are available under the MIT License.


help:
	@echo Valid targets are:
	@echo help - Prints this help message
	@echo code-check - Runs pycodestyle on all python code in the project
	@echo coverage - Use pytest to run all tests and report on test coverage
	@echo run - Runs coverter application
	@echo test - Use pytest to run all tests


VENV = venv

ifeq ($(OS),Windows_NT)
  CP = copy
  GIT_HOOKS_TARGET = .git\hooks\pre-commit
  GIT_HOOKS_SOURCE = git-hooks\pre-commit
  PROJECT_PYFILES = \
    setup.py \
    converter/conversion_manager.py \
    converter/filewriter.py \
    converter/logger.py \
    converter/main.py \

  PYTHON = python
  ACTIVATE = $(VENV)\Scripts\activate
  RMDIR_CMD := rmdir /s /q
  virtualenv = $(shell where virtualenv.exe)
else
  CP = cp
  GIT_HOOKS_TARGET = .git/hooks/pre-commit
  GIT_HOOKS_SOURCE = git-hooks/pre-commit
  PROJECT_PYFILES = *.py */*.py
  PYTHON = python3
  ACTIVATE_SCRIPT = $(VENV)/bin/activate
  ACTIVATE = export PYTHONPATH=.; . $(ACTIVATE_SCRIPT)
  RMDIR_CMD = rm -rf
  virtualenv = $(shell which virtualenv)
endif


$(GIT_HOOKS_TARGET): $(GIT_HOOKS_SOURCE)
	@$(CP) $(GIT_HOOKS_SOURCE) $(GIT_HOOKS_TARGET)


ifeq ($(virtualenv),)
  NEED_VIRTUALENV = virtualenv
endif

virtualenv:
	@pip install virtualenv


$(VENV): $(NEED_VIRTUALENV) requirements.txt $(GIT_HOOKS_TARGET)
	@-$(RMDIR_CMD) $(VENV)
	@virtualenv -p $(PYTHON) $@
	@$(ACTIVATE) && pip install -r requirements.txt


code-check: $(VENV)
	@$(ACTIVATE) && flake8 $(PROJECT_PYFILES)


run: $(VENV)
	@$(ACTIVATE) && $(PYTHON) -m converter.main


test: $(VENV)
	@$(ACTIVATE) && pytest


coverage: $(VENV)
	@$(ACTIVATE) ; pytest --cov=converter --cov-report=term --cov-report=html
