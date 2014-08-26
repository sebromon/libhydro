#------------------------------------------------------------------------------
# LIBHYDRO - tests makefile
#------------------------------------------------------------------------------
# All tests must be run from inside the test directory.
#------------------------------------------------------------------------------
# Author: Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>
# Version: 0.1a - 2014-08-26
# History:
#   V0.1 - 2014-08-01
#     first shot
#------------------------------------------------------------------------------
# TODO - run all tests with nosetests and coverage
#    clear; nosetests --with-coverage --cover-package=libhydro test*.py
# TODO - run all tests with unittest and warnings about Python3 incompatibilities
#    clear; python -3 -m unittest discover -p 'test*.py'
#------------------------------------------------------------------------------
SHELL = /bin/sh

TESTS_FILES := $(wildcard *.py)

default: help

.PHONY: t tests _tests_title ${TESTS_FILES}
t: tests
tests: _tests_title ${TESTS_FILES} clean
_tests_title:
	@echo
	@echo '---------------------------'
	@echo 'Run all tests with unittest'
	@echo '---------------------------'
	@echo
${TESTS_FILES}:
	@python -m unittest $(basename ${@})

.PHONY: d discover _discover
# The discover sub-command has the following options:
#     -v, --verbose                     Verbose output
#     -s, --start-directory directory   Directory to start discovery (. default)
#     -p, --pattern pattern             Pattern to match test files (test*.py default)
d: discover
discover: _discover clean
_discover:
	@echo
	@echo '---------------------------'
	@echo 'Run all tests with discover'
	@echo '---------------------------'
	@echo
	@python -m unittest discover -p 'test*.py'

.PHONY: c coverage _coverage
c: coverage
coverage: _coverage clean
_coverage:
	@echo
	@echo '----------------------------------------'
	@echo 'Run all tests with discover and coverage'
	@echo '----------------------------------------'
	@echo
	@coverage run -m unittest discover -p 'test*.py'; coverage report -m

.PHONY: clean
clean:
	@rm -rf *.pyc

.PHONY: help
help:
	@echo
	@echo '------------------'
	@echo 'Available commands'
	@echo '------------------'
	@echo
	@echo 'make c[overage]'
	@echo 'make clean'
	@echo 'make d[iscover]'
	@echo 'make t[ests]'
	@echo 'make [help]'
