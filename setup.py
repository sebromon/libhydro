# -*- coding: utf-8 -*-
"""Libhydro setup file."""
# -- imports ------------------------------------------------------------------
from setuptools import setup, find_packages
import os
import re
import codecs

# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1.7"""
__date__ = """2017-04-20"""

# HISTORY
# V0.1 - 2014-01-28
#   first shot


# -- functions ----------------------------------------------------------------
def find_version(*file_paths):
    """Return the version number from a source file.

    Open the file in Latin-1 so that we avoid encoding errors.
    Use codecs.open for Python 2 compatibility

    """
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


# -- main ---------------------------------------------------------------------
here = os.path.abspath(os.path.dirname(__file__))

try:
    with codecs.open('DESCRIPTION.rst', encoding='utf-8') as description:
        long_description = description.read()
except Exception:
    # description is not that important but we want users to execute
    # the setup program within the root directory
    print('Unable to find description in the local directory')
    exit(1)

setup(
    name='libhydro',
    version=find_version('libhydro', '__init__.py'),
    description='Librairie pour manipuler les objets des dictionnaires '
                'Hydrometrie du SANDRE',
    long_description=long_description,
    url='https://bitbucket.org/PhilippeGouin/libhydro/',
    download_url='https://bitbucket.org/PhilippeGouin/libhydro/downloads/'
                 'libhydro-{}.tar.gz'.format(
                     find_version('libhydro', '__init__.py')),
    author='Philippe Gouin',
    author_email='philippe.gouin@developpement-durable.gouv.fr',
    platforms=('any',),
    classifiers=[
        # refer to https://pypi.python.org/pypi?:action=list_classifiers
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Atmospheric Science :: Hydrology'],
    keywords=['hydrology'],
    packages=find_packages(exclude=["doc", "tests"]),
    install_requires=('numpy >= 1.7.1', 'pandas == 0.16', 'lxml >= 3.2.3'))
