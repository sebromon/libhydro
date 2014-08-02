#------------------------------------------------------------------------------
# LIBHYDRO - main makefile
#------------------------------------------------------------------------------
# Author: Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>
# Version: 0.1a - 2014-08-02
# History:
#   V0.1 - 2014-08-02
#     first shot
#------------------------------------------------------------------------------
# TODO - link the tests and doc Makefiles
#------------------------------------------------------------------------------
SHELL = /bin/sh

default: help

.PHONY: dist
dist:
	@echo
	@echo '-----------------------'
	@echo 'Create the distribution'
	@echo '-----------------------'
	@echo
	@python setup.py sdist

.PHONY: clean
clean:
	@echo
	@echo '-------------------'
	@echo 'Clean the pyc files'
	@echo '-------------------'
	@echo
	@find . -name '*.pyc' -exec rm {} \;

.PHONY: cleanall
cleanall:
	@echo
	@echo '---------------------------'
	@echo 'Clean the pyc and swp files'
	@echo '---------------------------'
	@echo
	@find . -name '*.pyc' -or -name '*.swp' -exec rm {} \;

.PHONY: help
help:
	@echo
	@echo '------------------'
	@echo 'Available commands'
	@echo '------------------'
	@echo
	@echo 'make dist'
	@echo 'make clean|cleanall'
	@echo 'make [help]'
