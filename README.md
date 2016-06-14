# bython
Python with braces. Because python is awesome, but whitespace is aweful.

Bython is a python preprosessor which translates curly brackets into indentation.



### key features
 * "Forget" about indentaition. You should still write beautiful code, but if you mess up with tabs/spaces, or copy one piece of code to another that uses a different indentation style, it won't break.

 * Runs on python, that means that all of your existing modules, like NumPy and Matplotlib still works.



### quick intro
Bython works by first translating bython-files (suggested file ending: .by) into python-files, and then using python to run them. You therefore need a working installation of python for bython to work.


To run a bython program, simply type

	> bython source.by

to run `source.by`. To compile multiple files just list them all:

	> bython source1.by source2.by ...

The first file listed will be executed, the rest will be translated from bython to python (useful for imports). 


If you want more details on how to run bython files (flags, etc), type

	> bython -h

to print the built-in help page.



### installation
Bython is currently only developed for Linux. To install simply download all the files in this repository, and run 

	> sudo make install

in the top directory. This will compile bython from source, copy the binaries to "/usr/local/bython" and create a symbolic link in "/usr/local/bin" so that bython is available from the shell. To uninstall, simply run 

	> sudo make uninstall

which will undo all the changes.

See the installation guide for more details.
