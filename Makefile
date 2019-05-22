VIRTUALENV = virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
TOX = $(VENV)/bin/tox
TEMPDIR := $(shell mktemp -d)

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -U pip
	$(TEMPDIR)/bin/pip install -Ue .
	$(TEMPDIR)/bin/pip freeze | grep -v -- '^-e' > requirements.txt

virtualenv: $(PYTHON)
$(PYTHON):
	virtualenv $(VENV)


tox: $(TOX)
$(TOX): virtualenv
	$(VENV)/bin/pip install -U pip tox black

tests-once: tox
	$(VENV)/bin/tox -e py27

tests: tox
	$(VENV)/bin/tox

black: tox
	$(VENV)/bin/black --exclude kinto_pusher tests setup.py
