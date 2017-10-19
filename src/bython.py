#! /usr/bin/python3
import parser
import argparse
import os

"""
Bython is Python with braces.

This is a command-line utility to translate and run bython files.

Flags:
    -v, --version:      Print version number
    -c, --compile:      Translate to python file and store; do not run
    -t, --lower_true:   Adds support for lower case true/false
    -2, --python2:      Use python2 instead of python3
    input,              Bython files to process
    args,               Arguments to script
"""

VERSION_NUMBER = "0.4"
HOME = os.path.expanduser("~")

def main():
    # Setup argument parser
    argparser = argparse.ArgumentParser("bython", 
        description="Bython is a python preprosessor that translates braces into indentation", 
        formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v", "--version", 
        action="version", 
        version="Bython v%s\nMathias Lohne and Tristan Pepin 2017" % VERSION_NUMBER)
    argparser.add_argument("-c", "--compile", 
        help="translate to python only (don't run files)",
        action="store_true")
    argparser.add_argument("-k", "--keep",
        help="keep generated python files",
        action="store_true")
    argparser.add_argument("-t", "--lower_true",
        help="adds support for lower case true/false",
        action="store_true")
    argparser.add_argument("-2", "--python2",
        help="use python2 instead of python3 (default)",
        action="store_true")
    argparser.add_argument("input",
        type=str, 
        help="bython files to process",
        nargs=1)
    argparser.add_argument("args",
        type=str,
        help="arguments to script",
        nargs=argparse.REMAINDER)

    # Parse arguments
    cmd_args = argparser.parse_args()

    # Where to output files
    if cmd_args.compile or cmd_args.keep:
        # Place in same folder, no path prefix
        placement_path = ""

    else:
        # Place in subfolder of home dir
        placement_path = HOME + "/.bythontemp/"

    # Translate bython to python
    parse_stack = []

    # Add all files from cmd line
    parse_stack.append(cmd_args.input[0])
    if cmd_args.compile:
        for arg in cmd_args.args:
            parse_stack.append(arg)

    # Add all files from imports, and recursivelly (ish) add all imports from
    # the imports (and so on..)
    i = 0
    while i < len(parse_stack):
        import_files = parser.parse_imports(parse_stack[i])

        for import_file in import_files:
            if os.path.isfile(import_file) and not import_file in parse_stack:
                parse_stack.append(import_file)

        i += 1

    # Parsing
    try:
        for file in parse_stack:
            current_file_name = file
            parser.parse_file(file, cmd_args.lower_true, placement_path)

    except (TypeError, FileNotFoundError) as e:
        print("Error while parsing file", current_file_name)
        # Cleanup
        try:
            for file in parse_stack:
                os.remove(placement_path + parser._change_file_name(file))
        except:
            pass

        return

    # Stop if we were only asked to translate
    if cmd_args.compile:
        return

    # Run file
    if cmd_args.python2:
        python_command = "python"

    else:
        python_command = "python3"

    os.system("%s %s %s" % (
        python_command,
        placement_path + parser._change_file_name(cmd_args.input[0]),
        " ".join(arg for arg in cmd_args.args))
    )

    # Delete file if requested
    if not cmd_args.keep:
        for file in parse_stack:
            os.remove(placement_path + parser._change_file_name(file))


if __name__ == '__main__':
    main()


