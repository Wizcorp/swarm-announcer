WORK_DIR = $(shell pwd)
VIRTUALENV = $(shell if hash virtualenv2 2>/dev/null; then \
	echo "virtualenv2"; \
else \
	echo "virtualenv"; \
fi)
PYTHON_VERSION = $(lastword $(sort $(wildcard $(addsuffix /python2.?,$(subst :, ,$(PATH))))))

# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: all clean deps run

all: clean deps

clean:
	rm -rf venv
	rm -f *.pyc

deps:
	@if [ -z "$(PYTHON_VERSION)" ]; then echo "error: couldn't find a valid version of python installed"; false; fi
	@if ! hash $(VIRTUALENV) 2>/dev/null; then echo "error: couldn't find a valid version of virtualenv installed"; false; fi
	if [ ! -d venv ]; then $(VIRTUALENV) --python=$(PYTHON_VERSION) venv; fi
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install --upgrade -r requirements.txt

run:
	./venv/bin/python announce.py $(RUN_ARGS)
