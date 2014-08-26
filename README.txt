Libhydro
===============================================================================

Overview
-------------------------------------------------------------------------------
A library to deal with Hydrometrie datas.

Get the library from Mercurial
-------------------------------------------------------------------------------
Clone the repo::
    hg clone https://PhilippeGouin@bitbucket.org/PhilippeGouin/libhydro

or upload a release (bz2, zip, gz) from the web page.

Building the distribution
-------------------------------------------------------------------------------
python setup.py sdist

Testing
-------------------------------------------------------------------------------
All tests must be run from inside the tests directory.

Run all test with unittest::
    python -m unittest discover -p 'test*.py'

    The discover sub-command has the following options:
        -v, --verbose                     Verbose output
        -s, --start-directory directory   Directory to start discovery (. default)
        -p, --pattern pattern             Pattern to match test files (test*.py default)

Run all test with unittest and coverage::
    coverage run -m unittest discover -p 'test*.py'; coverage report -m

Run all test with nosetests and coverage::
    nosetests --with-coverage --cover-package=libhydro test*.py

Contact
-------------------------------------------------------------------------------
Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>
