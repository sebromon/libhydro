#------------------------------------------------------------------------------
# MAKEFILE - V0.1a - 20130704
#------------------------------------------------------------------------------
# SOURCE: https://github.com/vital-fadeev/python-package-template
#------------------------------------------------------------------------------
# USAGE:
#    make test - run all tests
#    make deb - build Debian package
#    make source - build source tarball
#    make daily - make daily snapshot
#    make install - install program
#    make init - install all requirements
#    make clean - clean project, remove *.pyc and other templorary files
#    make deploy - create vitrual environment
#------------------------------------------------------------------------------

PYTHON=`which python`
NAME=`python setup.py --name`
VERSION=`python setup.py --version`
SDIST=dist/$(NAME)-$(VERSION).tar.gz
VENV=/tmp/venv


all: check test source deb

dist: source deb

source:
$(PYTHON) setup.py sdist

deb:
$(PYTHON) setup.py --command-packages=stdeb.command bdist_deb

rpm:
$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

install:
$(PYTHON) setup.py install --install-layout=deb

test:
unit2 discover -s tests -t .

check:
find . -name \*.py | grep -v "^test_" | xargs pylint --errors-only --reports=n
# pep8
# pyntch
# pyflakes
# pychecker
# pymetrics

upload:
$(PYTHON) setup.py sdist register upload
$(PYTHON) setup.py bdist_wininst upload

init:
pip install -r requirements.txt --use-mirrors

update:
rm ez_setup.py
wget http://peak.telecommunity.com/dist/ez_setup.py

daily:
$(PYTHON) setup.py bdist egg_info --tag-date

deploy:
# make sdist
rm -rf dist
python setup.py sdist

# setup venv
rm -rf $(VENV)
virtualenv --no-site-packages $(VENV)
$(VENV)/bin/pip install $(SDIST)

clean:
$(PYTHON) setup.py clean
rm -rf build/ MANIFEST dist build my_program.egg-info deb_dist
find . -name '*.pyc' -delete
