# Bython
Python with braces. Because Python is awesome, but whitespace is awful.

Bython is a Python preprosessor which translates curly brackets into indentation.


## Content of README:
  * [Key features](#key-features)
  * [Code example](#code-example)
  * [Installation](#installation)
  * [Quick intro](#quick-intro)
  * [Structure of the repository](#structure-of-the-repository)


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


## Installation
You can install Bython directly from PyPI using pip:

	> sudo -H pip3 install bython

If you for some reason want to install it from the git repository you can use `git clone` and do a local install instead:

	> git clone https://github.com/mathialo/bython.git
	> cd bython
	> sudo -H pip3 install .

The git version is sometimes a tiny bit ahead of the PyPI version, but not significantly.

To uninstall, simply run 

	> sudo pip3 uninstall bython

which will undo all the changes.



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

For a more in-depth intro, consult the [bython introduction](INTRODUCTION.md)


## Structure of the repository
At the moment, Bython is written in Python. The git repository is structured into 4 directories:

 * `bython` contains a Python package containing the parser and other utilities used by the main script
 * `etc` contains manual pages and other auxillary files
 * `scripts` contains the runnable Python scripts, ie the ones run from the shell
 * `testcases` contains a couple of sample \*.by and \*.py files intended for testing the implementation

