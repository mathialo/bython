import re
import os

"""
parser.py

Python module for converting bython code to python code.

Usage:
    parse_file(filename, add_true_line)
"""

def _ends_in_by(word):
    """Return true if the string 'word' ends in '.by'"""
    return word[-3:] == ".by"


def _change_file_name(name):
    """Adds .by to the end of the string name, changing .py to .by"""
    if _ends_in_by(name):
        return name[:-3] + ".py"

    else:
        return name + ".py"


def parse_imports(filename):
    """
    Reads the file, and scans for imports. Returns all the assumed filename
    of all the imported modules (ie, module name appended with ".by")
    """
    infile = open(filename, 'r')
    infile_str = ""

    for line in infile:
        infile_str += line


    imports = re.findall(r"(?<=import\s)[\w.]+(?=;|\s|$)", infile_str)

    imports_with_suffixes = [im + ".by" for im in imports]

    return imports_with_suffixes


def parse_file(filename, add_true_line, placement_path):
    """
    Converts a bython file to a python file and writes it to disk.
    
    filename is a string pointing to the .by file you want to parse.
    
    add_true_line is a True/False value. If True, "true" and "false",
    "true = True" and "false = False" are defined in the resulting
    python file.

    placement_path is where the directory where the output files should
    be stored. 
    """
    if not placement_path == "":
        os.makedirs(os.path.dirname(placement_path), exist_ok=True)

    infile = open(filename, 'r')
    outfile = open(placement_path + _change_file_name(filename), 'w')

    indentation_level = 0
    indentation_sign = "    "

    if add_true_line:
        outfile.write("true=True; false=False;\n")

    # Read file to string
    infile_str_raw = ""
    for line in infile:
        infile_str_raw += line

    # Add 'pass' where there is only a {}
    infile_str_raw = re.sub(r"{[\s\n\r]*}", "{\npass\n}", infile_str_raw)

    # Fix indentation
    infile_str_indented = ""
    for line in infile_str_raw.split("\n"):
        # skip empty lines:
        if line in ('\n', '\r\n'):
            infile_str_indented += line + "\n"
            continue

        # remove existing whitespace:
        line = line.lstrip()
        
        # Check for reduced indent level
        for i in list(line):
            if i == "}":
                indentation_level -= 1

        # Add indentation
        for i in range(indentation_level):
            line = indentation_sign + line

        # Check for increased indentation
        for i in list(line):
            if i == "{":
                indentation_level += 1

        infile_str_indented += line + "\n"

    # Replace { with : and remove }
    infile_str_indented = re.sub(r"[\t ]*{[ \t]*", ":", infile_str_indented)
    infile_str_indented = re.sub(r"}[ \t]*", "", infile_str_indented)
    infile_str_indented = re.sub(r"\n:", ":", infile_str_indented)

    # Support for extra, non-brace related stuff
    infile_str_indented = re.sub(r"else\s+if", "elif", infile_str_indented)
    infile_str_indented = re.sub(r";\n", "\n", infile_str_indented)

    outfile.write(infile_str_indented)

    infile.close()
    outfile.close()
