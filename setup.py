# -*- coding: utf-8 -*-
"""Libhydro setup file."""
#-- imports -------------------------------------------------------------------
from setuptools import setup, find_packages
import os
import re

# work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
# try:
#     codecs.lookup('mbcs')
# except LookupError:
#     ascii = codecs.lookup('ascii')
#     func = lambda name, enc = ascii: {True: enc}.get(name == 'mbcs')
#     codecs.register(func)

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1e"""
__date__ = """2014-08-26"""

#HISTORY
#V0.1 - 2014-01-28
#    first shot


# -- functions ----------------------------------------------------------------
def find_version(*file_paths):
    """Return the version number from a source file.

    Open the file in Latin-1 so that we avoid encoding errors.
    Use codecs.open for Python 2 compatibility

    """
    # Read the file
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form __version__ = 'ver'
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)

    # Not found case
    raise RuntimeError("Unable to find version string.")


# -- main ---------------------------------------------------------------------
# Get the local dir
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as description:
    long_description = description.read()

# Setup
setup(
    name='libhydro',
    version=find_version('libhydro', '__init__.py'),
    description='Librairie pour manipuler les objets des dictionnaires '
                'Hydrometrie du SANDRE',
    long_description=long_description,
    url='https://bitbucket.org/PhilippeGouin/libhydro/',
    download_url='https://bitbucket.org/PhilippeGouin/libhydro/downloads/'
                 'libhydro-{}.tar.gz'.format(
                     find_version('libhydro', '__init__.py')
                 ),
    author='Philippe Gouin',
    author_email='philippe.gouin@developpement-durable.gouv.fr',
    # maintainer
    # maintainer_email
    # license='MIT',
    platforms=('any',),
    classifiers=[
        #refer to https://pypi.python.org/pypi?:action=list_classifiers
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Atmospheric Science :: Hydrology',
    ],

    # What does your project relate to?
    keywords=['hydrology'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["doc", "tests"]),
    # If there are data files included in your packages, specify them here.
    # package_data={
    #    'sample': ['*.dat'],
    # },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    install_requires=(
        'python >= 2.7, <3',
        'numpy >= 1.7.1',
        'pandas >= 0.11.0',
        'lxml >= 3.2.3',
        'suds-jurko >= 0.6'
    ),
)
