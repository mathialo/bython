# Bython
Python with braces. Because Python is awesome, but whitespace is awful.

Bython is a Python preprosessor which translates curly brackets into indentation.



## Key features
 * "Forget" about indentaition. You should still write beautiful code, but if you mess up with tabs/spaces, or copy one piece of code to another that uses a different indentation style, it won't break.

 * Runs on Python, that means that all of your existing modules, like NumPy and Matplotlib still works.


## Code example
```python
def print_message(num_of_times) {
    for i in range(num_of_times) {
        print("Bython is awesome!");
    }
}

if __name__ == "__main__" {
    print_message(10);
}
```



## Quick intro
Bython works by first translating Bython-files (suggested file ending: .by) into Python-files, and then using Python to run them. You therefore need a working installation of Python for Bython to work.


To run a Bython program, simply type

	> bython source.by arg1 arg2 ...

to run `source.by` with arg1, arg2, ... as command line arguments. If you want more details on how to run Bython files (flags, etc), type

	> bython -h

to print the built-in help page. You can also consult the man page by typing

	> man bython

Bython also includes a translator from Python to Bython. This is found via the `py2by` command:

	> py2by test.py

This will create a Bython file called `test.by`. A full explanation of `py2by`, is found by typing

	> py2by -h

or by consulting the man page:

	> man py2by


## Installation
Bython is currently only developed for Unix-like OS's. To install simply open a terminal, move to a suited directory (like Downloads), and type
	
	> git clone https://github.com/mathialo/bython.git
	> cd bython
	> sudo make install

This will copy the executables to "/usr/local/bython" and create a symbolic link in "/usr/local/bin" so that Bython is available from the shell. To uninstall, simply run 

	> sudo make uninstall

which will undo all the changes.


### Custom install dir
Bython will automatically install itself to "/usr/local/bython/". If you for some reason want to change this, open the Makefile in the top directory and change the line (no 1):
``` 
INSTALL_DIR = /usr/local/bython/
```
to be whereever you want. The file copying and link creation will now use your new directory.


