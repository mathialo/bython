# bython
Python with braces. Because python is awesome, but whitespace is awful.

Bython is a python preprosessor which translates curly brackets into indentation.



### key features
 * "Forget" about indentaition. You should still write beautiful code, but if you mess up with tabs/spaces, or copy one piece of code to another that uses a different indentation style, it won't break.

 * Runs on python, that means that all of your existing modules, like NumPy and Matplotlib still works.



### quick intro
Bython works by first translating bython-files (suggested file ending: .by) into python-files, and then using python to run them. You therefore need a working installation of python for bython to work.


To run a bython program, simply type

	> bython source.by arg1 arg2 ...

to run `source.by` with arg1, arg2, ... as command line arguments. To compile multiple files, list them all with the -m flag:

	> bython -m source1.by source2.by ...

This is useful for imports. Notice that the -m flag has been added. It stands for multiple files, and tells bython to treat all the words in the command as filenames instead of cmd-line args.


If you want more details on how to run bython files (flags, etc), type

	> bython -h

to print the built-in help page.



### installation
Bython is currently only developed for Linux. To install simply open a terminal, move to a suited directory (like Downloads), and type
	
	> git clone https://github.com/mathialo/bython.git
	> cd bython
	> sudo make install
	
If you allready have an installation of bython, but have downloaded a new version and want to update, type

	> sudo make update

This will compile bython from source, copy the binaries to "/usr/local/bython" and create a symbolic link in "/usr/local/bin" so that bython is available from the shell. To uninstall, simply run 

	> sudo make uninstall

which will undo all the changes.


#### custom install dir
Bython will automatically install itself to "/usr/local/bython/". If you for some reason want to change this, open the Makefile in the top directory and change the line (no 1):
``` 
INSTALL_DIR = /usr/local/bython/
```
to be whereever you want. The file copying and link creation will now use your new directory.
