# which is bash on Fedora
SHELL = /bin/sh

.PHONY: backup dist doc test clean cleanall help

default: help

backup: cleanall
	@echo
	@echo '-----------------------'
	@echo 'Backup the repo'
	@echo '-----------------------'
	@echo
	# check destination
	@set -e
	@if test -z "${DEST}"; then echo 'missing DEST dir'; exit 1; fi
	@if test ! -d "${DEST}"; then echo 'unknown DEST dir'; exit 1; fi
	# backup to ${DEST}
	@tar cjf ${DEST}/libhydro_$(shell date +%Y%m%d).tar.bz2 -C '..' $(shell basename ${PWD})

dist:
	@echo
	@echo '-----------------------'
	@echo 'Create the distribution'
	@echo '-----------------------'
	@echo
	@python setup.py sdist --format=gztar
	@python setup.py sdist --format=zip
	@python setup.py bdist_wheel
	@# FIXME - @python setup.py bdist_wininst

doc:
	@cd doc && $(MAKE) all

test:
	@echo
	@$(MAKE) discover -C test

clean:
	@echo
	@echo '-------------------'
	@echo 'Clean the pyc files'
	@echo '-------------------'
	@echo
	@find . -name '*.pyc' -exec rm {} \;

cleanall:
	@echo
	@echo '---------------------------'
	@echo 'Clean everything'
	@echo '---------------------------'
	@echo
	# remove the pyc and the swap files
	@find . -name '*.pyc' -or -name '*.swp' -exec rm {} \;
	# remove the build and the libhydro.egg-info dirs
	@rm -rf ./build ./libhydro.egg-info

help:
	@echo
	@echo '------------------'
	@echo 'Available commands'
	@echo '------------------'
	@echo
	@echo 'make backup DEST=<directory>'
	@echo 'make clean|cleanall'
	@echo 'make dist'
	@echo 'make doc'
	@echo 'make test'
	@echo 'make [help]'
