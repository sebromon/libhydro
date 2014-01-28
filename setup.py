#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Libhydro setup file."""
#-- imports -------------------------------------------------------------------
# from ez_setup import use_setuptools
# use_setuptools()
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-01-28"""

#HISTORY
#V0.1 - 2014-01-28
#    first shot


#-- todos ---------------------------------------------------------------------
# setup test
# include doc


# -- setup --------------------------------------------------------------------
# -- prepare --
tmp_files_to_remove = []
# distutil needs a README file while hg requires a md file
if not os.path.isfile('README'):
    try:
        os.link('README.md', 'README')
        tmp_files_to_remove.append('README')
    except OSError:
        pass

# -- main config --
setup(
    name='libhydro',
    version='0.2.0',
    author='Philippe Gouin',
    author_email='philippe.gouin@developpement-durable.gouv.fr',
    # maintainer
    # maintainer_email
    description='Librairie pour manipuler les objets des dictionnaires '
                'Hydrométrie du SANDRE',
    long_description=open('README').read(),
    # classifiers
    platforms=('any',),
    # license  # TODO
    # url='unknown',  # TODO - what is the download_url tag ?
    packages=['core', 'conv', 'conv/shom', 'conv/xml'],
    # data_files=[
    #     ('', ['__init__.py']),
    # ],
    # package_data={'mypkg': ['data/*.dat']},  # FIXME - tests data
    install_requires=(
        'python >= 2.7',
        'numpy >= 1.7.1',
        'pandas >= 0.11.0',
        'lxml >= 3.2.3'
    )
)

# -- clean everything --
for f in tmp_files_to_remove:
    try:
        os.remove(f)
    except OSError:
        pass
