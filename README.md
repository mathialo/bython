# Bython
Python with braces. Because Python is awesome, but whitespace is awful.

Bython is a Python preprosessor which translates curly brackets into indentation.



## Key features
 * "Forget" about indentaition. You should still write beautiful code, but if you mess up with tabs/spaces, or copy one piece of code to another that uses a different indentation style, it won't break.

 * Uses Python for interpretation, that means that all of your existing modules, like NumPy and Matplotlib still works.


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
	> sudo pip3 install .

This will copy the executables to "/usr/local/bin" so that Bython is available from the shell. To uninstall, simply run 

	> sudo pip3 uninstall bython

which will undo all the changes.


## Structure of the repository
At the moment, Bython is written in Python. The git repository is structured into 4 directories:

 * `bython` contains a Python package containing the parser and other utilities used by the main script
 * `etc` contains manual pages and other auxillary files
 * `scripts` contains the runnable Python scripts, ie the ones run from the shell
 * `testcases` contains a couple of sample \*.by and \*.py files intended for testing the implementation

