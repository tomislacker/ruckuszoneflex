PY_VERSION := 2.7
VENV_PATH := venv

LOG_LEVEL := ERROR
TEST_FAST := --fail-fast
TEST_ARGS := 

venv:
	virtualenv -p python$(PY_VERSION) $(VENV_PATH)

.PHONY : dev
dev    : venv
	$(VENV_PATH)/bin/pip install -r requirements.txt
	$(VENV_PATH)/bin/pip install -r requirements-dev.txt

.PHONY   : notebook
notebook : dev
	$(VENV_PATH)/bin/jupyter-notebook

.PHONY : test
test   : dev
	@$(VENV_PATH)/bin/nose2 \
		-vv \
		--log-level $(LOG_LEVEL) \
		$(TEST_FAST) \
		$(TEST_ARGS)
