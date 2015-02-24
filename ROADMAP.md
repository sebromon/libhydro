Libhydro road map
===============================================================================

Functionalities
-------------------------------------------------------------------------------
* Write the CSV Sandre converter
* Add support for Bdhydro WS connection
* Implement some of the computations described in:
    http://ambhas.com/books/python-in-hydrology/book.html#Q1-1-174?utm_medium=referral&utm_source=pulsenews
* Add functionnalities to check/update the Nomenclature cache automatically from the Sandre

Performances
-------------------------------------------------------------------------------
* Write some tests first and analyze (but a lighter version of the classes using
Pandas containers should be more efficient for those who use only the converters)

Tests
-------------------------------------------------------------------------------
* Tests should be running from the main makefile

Deployment
-------------------------------------------------------------------------------
* We should be able to build with bdist win32 on a linux machine
