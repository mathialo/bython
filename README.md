# bython
Python with braces. Because python is awesome, but whitespace is aweful.

Bython is a python preprosessor which translates braces into indentation.

## quick intro
Bython works by first translating bython-files (suggested file ending: .by) into python-files, and then using python to run them. You therefore need a working installation of python for bython to work.

To run a bython program, simply type "bython source.by" to run source.by. To compile multiple files just list them all: "bython source1.by source2.by ...". The first file listed will be executed, the rest will be translated from bython to python (useful for imports). 

Since it's built on python, all of your existing modules (like numpy) will work.


## installation
Bython is currently only developed for Linux. To install simply download all the files in this repository, and run "sudo make install". This will compile bython from source, copy the binaries to /usr/local/bython and create a symbolic link in /usr/local/bin so that bython is available from the shell. To uninstall, simply run "sudo make uninstall" which will undo all the changes.
