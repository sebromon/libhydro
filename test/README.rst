All tests must be run from inside the test directory.

Run all test with unittest::
    clear; python -m unittest discover -p 'test*.py'

    The discover sub-command has the following options:
        -v, --verbose                     Verbose output
        -s, --start-directory directory   Directory to start discovery (. default)
        -p, --pattern pattern             Pattern to match test files (test*.py default)

Run all test with unittest and coverage::
    clear; coverage run -m unittest discover -p 'test*.py'; coverage report -m

Run all test with nosetests and coverage::
    clear; nosetests --with-coverage --cover-package=libhydro test*.py
