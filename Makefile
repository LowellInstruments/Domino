# Adapted from various Makefiles from projects under
# https://github.com/masschallenge.
# All aspects that are copyrighted by MassChallenge or Nathan Wilson
# are available under the MIT License.

target_help = \
  "help - Prints this help message" \
  "" \
  "code-check - Runs pycodestyle on all python code in the project" \
  "coverage - Use pytest to run all tests and report on test coverage" \
  "run - Runs the script using LOG (default /var/log/access.log) and" \
  "\tTHRESHOLD (default 10). See README.md for more options." \
  "test - Use pytest to run all tests" \


GIT_HOOKS_TARGET_DIR = .git/hooks/
GIT_HOOKS_SOURCE_DIR = git-hooks/
GIT_HOOKS_FILES = pre-commit
GIT_HOOKS_TARGETS = $(addprefix $(GIT_HOOKS_TARGET_DIR),$(GIT_HOOKS_FILES))
GIT_HOOKS_SOURCES = $(addprefix $(GIT_HOOKS_SOURCE_DIR),$(GIT_HOOKS_FILES))

$(GIT_HOOKS_TARGET_DIR)%: $(GIT_HOOKS_SOURCE_DIR)%
	@mkdir -p $(GIT_HOOKS_SOURCE_DIR)
	@cp $< $@


help:
	@echo "Valid targets are:\n"
	@for t in $(target_help) ; do \
	    echo $$t; done
	@echo


PROJECT_PYFILES = *.py log_parser/*.py tests/*.py
VENV = venv
ACTIVATE_SCRIPT = $(VENV)/bin/activate
ACTIVATE = export PYTHONPATH=.; . $(ACTIVATE_SCRIPT)

virtualenv = $(shell which virtualenv)

ifeq ($(virtualenv),)
  NEED_VIRTUALENV = virtualenv
endif

virtualenv:
	@sudo apt install virtualenv


$(VENV): $(NEED_VIRTUALENV) Makefile requirements.txt $(GIT_HOOKS_TARGETS)
	@rm -rf $(VENV)
	@virtualenv -p `which python3` $@
	@touch $(ACTIVATE_SCRIPT)
	@$(ACTIVATE) ; pip install -r requirements.txt


code-check: $(VENV)
	@$(ACTIVATE) ; flake8 $(PROJECT_PYFILES)


run: $(VENV)
	@$(ACTIVATE) ; python3 -m converter.main


test: $(VENV)
	@$(ACTIVATE) ; pytest


coverage: $(VENV)
	@$(ACTIVATE) ; pytest --cov=log_parser --cov-report=term --cov-report=html
