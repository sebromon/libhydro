#------------------------------------------------------------------------------
# LIBHYDRO - main makefile
#------------------------------------------------------------------------------
# Author: Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>
# Version: 0.2b - 2015-02-23
# History:
#   V0.2 - 2014-08-26
#     add the wheel dist
#     add the backup and the doc targets
#   V0.1 - 2014-08-02
#     first shot
#------------------------------------------------------------------------------
# TODO - link the tests and doc Makefiles
#------------------------------------------------------------------------------
SHELL = /bin/sh
BACKUP_DST := '/mnt/vosges2/gouinph/developpements/libhydro/libhydro'

default: help

.PHONY: backup
backup:
	@echo
	@echo '-----------------------'
	@echo 'Backup the repo'
	@echo '-----------------------'
	@echo
	tar cjf ${BACKUP_DST}_$(shell date +%Y%m%d).tar.bz2 .

.PHONY: dist
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

.PHONY: doc
doc:
	@cd doc && $(MAKE) all

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
	@echo 'Clean everything'
	@echo '---------------------------'
	@echo
	# remove the pyc and the swap files
	@find . -name '*.pyc' -or -name '*.swp' -exec rm {} \;
	# remove the build and the libhydro.egg-info dirs
	@rm -rf ./build ./libhydro.egg-info

.PHONY: help
help:
	@echo
	@echo '------------------'
	@echo 'Available commands'
	@echo '------------------'
	@echo
	@echo 'make backup'
	@echo 'make clean|cleanall'
	@echo 'make dist'
	@echo 'make doc'
	@echo 'make [help]'
