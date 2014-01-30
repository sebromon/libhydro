# -*- coding: utf-8 -*-
"""Libhydro setup file."""
#-- imports -------------------------------------------------------------------
from setuptools import setup, find_packages
import os
import re
import codecs


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2014-01-30"""

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
with open('DESCRIPTION.rst') as f:
    long_description = f.read()

# Setup
setup(
    name='libhydro',
    version=find_version('libhydro', '__init__.py'),
    description='Librairie pour manipuler les objets des dictionnaires '
                'Hydrometrie du SANDRE',
    long_description=long_description,
    url='http://arc.schapi:8001',
    author='Philippe Gouin',
    author_email='philippe.gouin@developpement-durable.gouv.fr',
    # maintainer
    # maintainer_email
    # license='MIT',
    platforms=('any',),
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
    ],

    # What does your project relate to?
    keywords='hydrology',

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
        'python >= 2.7',
        'numpy >= 1.7.1',
        'pandas >= 0.11.0',
        'lxml >= 3.2.3'
    ),
)
