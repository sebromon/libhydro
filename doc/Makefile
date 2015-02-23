#------------------------------------------------------------------------------
# LIBHYDRO - documentation makefile
#------------------------------------------------------------------------------
# Documentation is build in a local directory, compressed and moved to ../dist
# Pandoc to pdf should need the xelatex engine:
#     yum install texlive texlive-latex texlive-xetex texlive-collection-latex
#                 texlive-collection-latexrecommended texlive-xetex-def
#                 texlive-collection-xetex#
#------------------------------------------------------------------------------
# Author: Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>
# Version: 0.1c - 2014-08-25
# History:
#   V0.1 - 2014-07-29
#     first shot
#------------------------------------------------------------------------------
# TODO - the pdf files are not very pretty, the toc glue on the first page
# TODO - and the links are hidden
#------------------------------------------------------------------------------
SHELL = /bin/sh

RELEASE := $(shell unset GREP_OPTIONS; grep 'version' '../libhydro/__init__.py'|cut -c 16-20)
DST := libhydro-${RELEASE}_documentation

default: help

doc: all

.PHONY: all
all: pdf html
	@echo
	@echo '-----------------------'
	@echo 'Compress and distribute'
	@echo '-----------------------'
	@echo
	tar czf ${DST}.tar.gz ${DST}
	mv -i ${DST}.tar.gz ../dist
	rm -rf ${DST}

.PHONY: pdf
pdf: _subdir installation_guide_windows.md installation_guide_linux.md development_guide/notebooks/tutorial.ipynb
	@echo
	@echo '---------------------------'
	@echo 'Build the PDF documentation'
	@echo '---------------------------'
	@echo
	@# installation guide
	rm -rf ${DST}/installation_guide*.pdf ${DST}/tutorial.pdf
	@pandoc --toc installation_guide_windows.md -o ${DST}/installation_guide_windows.pdf
	@pandoc --toc installation_guide_linux.md -o ${DST}/installation_guide_linux.pdf
	@# tutorial
	@ipython2 nbconvert --to markdown development_guide/notebooks/tutorial.ipynb
	@pandoc tutorial.md -o ${DST}/tutorial.pdf --latex-engine=xelatex
	@rm -rf tutorial.md tutorial_files

.PHONY: html
.ONESHELL:
html: _subdir
	@echo
	@echo '---------------------------'
	@echo 'Build the API documentation'
	@echo '---------------------------'
	@echo
	@mkdir -p ${DST}/api
	@cd ${DST}/api
	@rm -f *.html
	@# -- index --
	@python -m pydoc -w libhydro
	@mv libhydro.html index.html
	@# -- core --
	@python -m pydoc -w libhydro.core
	@# core/alarm
	@# core/courbecorrection
	@# core/courbetarage
	@python -m pydoc -w libhydro.core.evenement
	@# core/gradienthydro
	@python -m pydoc -w libhydro.core.intervenant
	@#core/jaugeage
	@python -m pydoc -w libhydro.core.modeleprevision
	@python -m pydoc -w libhydro.core.nomenclature
	@# python -m pydoc -w libhydro.core.obselaboreehydro
	@python -m pydoc -w libhydro.core.obshydro
	@python -m pydoc -w libhydro.core.obsmeteo
	@# core/qualifannee
	@python -m pydoc -w libhydro.core.seuil
	@python -m pydoc -w libhydro.core.simulation
	@python -m pydoc -w libhydro.core.sitehydro
	@python -m pydoc -w libhydro.core.sitemeteo
	@# -- conv --
	@python -m pydoc -w libhydro.conv
	@python -m pydoc -w libhydro.conv.shom
	@python -m pydoc -w libhydro.conv.xml

.PHONY: clean
clean:
	@rm -rf ${DST}
	@rm -rf ${DST}.tar.gz

.PHONY: _subdir
_subdir:
	@mkdir -p ${DST}

.PHONY: help
help:
	@echo
	@echo '------------------'
	@echo 'Available commands'
	@echo '------------------'
	@echo
	@echo 'make all|doc'
	@echo 'make pdf'
	@echo 'make html'
	@echo 'make clean'
	@echo 'make [help]'
