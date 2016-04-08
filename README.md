# bython
Python with braces. Because python is awesome, but whitespace is aweful.

Bython is a python preprosessor which translates braces into indentation.

## quick intro
Bython works by first translating bython-files (suggested file ending: .by) into python-files, and then using python to run them. You therefore need a working installation of python for bython to work.

To run a bython program, simply type "bython source.by" to run source.by. To compile multiple files just list them all: "bython source1.by source2.by ...". The first file listed will be executed, the rest will be translated from bython to python (useful for imports). 

Since it's built on python, all of your existing modules (like numpy) will work.


## installation
Currently there are only binaries for linux, but you can try to compile from source if you don't run linux. Once you have binaries simply place the bython executable and the bython.py file in the same folder and add that folder to your system's PATH-variable. Alternatively you can make a link in a directory that already exists in the PATH-variable, like /usr/local/bin. 
