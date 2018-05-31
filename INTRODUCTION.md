# An introduction to Bython
This document gives a more thorough introduction to Bython.

## Table of contents

  * [0 - Installation](#0---installation)
  * [1 - The basics](#1---the-basics)
    * [1.1 - Running your program](#11---running-your-program)
    * [1.2 - Keeping generated Python files](#12---keeping-generated-python-files)
    * [1.3 - Different Python versions](#13---different-python-versions)
  * [2 - Differences from regular Python](#2---differences-from-regular-python)
    * [2.1 - Dictionaries](#21---dictionaries)
    * [2.2 - else if](#22---else-if)
  * [3 - Imports](#3---imports)
    * [3.1 - Importing Bython modules in Bython code](#31---importing-bython-modules-in-bython-code)
    * [3.2 - Importing Python modules in Bython code](#32---importing-python-modules-in-bython-code)
    * [3.3 - Importing Bython modules in Python code](#33---importing-bython-modules-in-python-code)    
  * [4 - Python files](#4---python-files)
    * [4.1 - Formatting of resulting Python files](#41---formatting-of-resulting-python-files)
    * [4.2 - Translating Python to Bython](#42---translating-python-to-bython)


# 0 - Installation
Bython is available from PyPI, so a call to pip should do the trick:

``` bash
$ sudo -H pip3 install bython
```

Bython should now be available from the shell.

# 1 - The basics
Bython is pretty much Python, but instead of using colons and indentation to create blocks of code, we instead use curly braces. A simple example of some Bython code should make this clear:

``` python
import numpy as np
import matplotlib.pyplot as plt

def plot_sine_wave(xmin=0, xmax=2*np.pi, points=100, filename=None) {
    xs = np.linspace(xmin, xmax, points)
    ys = np.sin(xs)

    plt.plot(xs, ys)

    if filename is not None {
        plt.savefig(filename)
    }

    plt.show()
}

if __name__ == "__main__" {
    plot_sine_wave()
}
```

Curly braces are used whenever colons and indentation would be used in regular Python, ie function/class definitions, loops, if-statements, ...

As you can see in the example above, importing modules from Python is no issue. All packages installed with your normal Python installation is available in Bython as well. 


## 1.1 - Running your program
Say we have written the above program, and saved it as `test.by`. To parse and run the program, use the `bython` command in the shell
``` bash
bython test.by
```
A plot containing one period of a sine wave should appear.


## 1.2 - Keeping generated Python files
Bython works by first translating your Bython files to regular Python, and then use Python to run it. After running, the created Python files are deleted. If you want to keep the created files after running, use the `-k` (k for 'keep') flag:
``` bash
bython -k test.by
```
If you don't want the program to be run, but only translated to Python, use the `-c` flag (c for 'compile'):
``` bash
bython -c test.by
```
In both cases, a file called `test.py` will remain in the directory you are working from.

If you want more control on the resulting outputfile, you can use the `-o` flag to specify the output file:
``` bash
bython -c -o out/python_test.py test.by
```


## 1.3 - Different Python versions
Bython is written in Python 3, so you need a working installation of Python 3.x to run Bython. Your Bython files, however, can be run in whatever Python version you prefer. The standard is Python 3 (ie, Bython will use the env command `python3` to run your program), but if you for legacy reasons want to run Python 2 instead, you can use the `-2` flag to do that:
``` bash
bython -2 test.by
```

# 2 - Differences from regular Python
Bython is created to be as similar to Python as possible, but there are a few important differences.

## 2.1 - Dictionaries
Since Python uses curly braces to define dictionaries, they create an issue with Bython. Using the standard `dict = {"one": 1, "two": 2}`-notation will create an error with Bython. Users are advised to use the constructor for the `dict` class instead (see [python documentation](https://docs.python.org/3/library/stdtypes.html#dict)). Some example ways to create dictionoaries in Bython:
``` python
# Only works if keys are strings:
dict1 = dict(one=1, two=2, three=3)

# Works in all cases:
dict2 = dict([("one", 1), ("two", 2), ("tree", 3)]) 
```

## 2.2 - else if
The standard way of creating if-chains in Python is with the `elif` keyword:

``` python
if x > 5:
    print("value is bigger than 5")
elif x == 5:
    print("value is 5")
else:
    print("value is smaller than 5")
```

Bython introduces C-style `else if` as an additional alternative. Normal `elif` is of course still valid:
``` python
# Python-style 'elif':
if x > 5 {
    print("value is bigger than 5")
} elif x == 5 {
    print("value is 5")
} else {
    print("value is smaller than 5")
}

# C-style 'else if'
if x > 5 {
    print("value is bigger than 5")
} else if x == 5 {
    print("value is 5")
} else {
    print("value is smaller than 5")
}
```

Both are valid and will work.


# 3 - Imports
Bython handles imports quite well. In this section we will look at the different scenarios where imports might occur.

## 3.1 - Importing Bython modules in Bython code
Importing Bython into Bython is not an issue at all. Before parsing the source file, Bython will also look for imports and automatically parse them as well. Say we have these two bython files:

main.by:
``` python
import test_module

test_module.func()
```

test_module.by:
``` python
def func() {
    print("hello!")
}
```

When running
``` bash
$ bython main.by
```

Bython will detect that test_module is imported and look for a file named `test_module.by` and parse that as well. This will also handle additional imports from `test_module.by`, and so on. It will also avoid circular imports.

## 3.2 - Importing Python modules in Bython code
As illustrated in the example in Section 1, Bython will automatically work with any Python modules/packages you have installed.

Local imports from Python files in the same directory is no issue either.


## 3.3 - Importing Bython modules in Python code
Importing Bython code into Python is a bit more tricky, but still quite streamlined. To import Bython modules in Python, you must use the `bython_import` function from the `bython.importing` module. Assume that the `test_module.by` file described in Section 3.1 is avaliable. To import it in a Python file, you can do as follows:
```python
from bython.importing import bython_import
bython_import("test_module", globals())

# The module is now available as test_module:
test_module.func()
```



# 4 - Python files

## 4.1 - Formatting of resulting Python files
Bython tries to keep the line numbers in the resulting Python files equivalent to the ones in the original source file. Thus, if an error occurs on line 42 when running Python, you can go to line 42 in the Bython code to inspect the error. 

However, this approach yields some undesirable formatting on the resulting Python code. You should therefore consider using some Python formatter like [yapf](https://github.com/google/yapf) or [black](https://github.com/ambv/black) on the output from Bython to make the resulting Python code nice and tidy. 



## 4.2 - Translating Python to Bython
If you want to translate Python code to Bython, you can use the built-in `py2by` script. It's an experimental feature, but seems to work quite well. 
