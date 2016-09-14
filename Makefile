PY_VERSION := 2.7
VENV_PATH := venv

venv:
	virtualenv -p python$(PY_VERSION) $(VENV_PATH)

.PHONY : dev
dev    : venv
	$(VENV_PATH)/bin/pip install -r requirements.txt
	$(VENV_PATH)/bin/pip install -r requirements-dev.txt

.PHONY   : notebook
notebook : dev
	$(VENV_PATH)/bin/jupyter-notebook
