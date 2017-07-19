#! /usr/bin/python3
import parser
import argparse
import os

VERSION_NUMBER = "0.3.1"


def main():
    # Setup argument parser
    argparser = argparse.ArgumentParser("bython", description="Bython is a python preprosessor that translates braces into indentation", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v", "--version", action="version", version="Bython v%s\nMathias Lohne 2017" % VERSION_NUMBER)
    argparser.add_argument("-c", "--compile", help="translate to python only (don't run files)", action="store_true")
    argparser.add_argument("-m", "--multiple", help="treat arguments as additional files to process", action="store_true")
    argparser.add_argument("-k", "--keep", help="keep generated python files", action="store_true")
    argparser.add_argument("-t", "--lower_true", help="adds support for lower case true/false", action="store_true")
    argparser.add_argument("-2", "--python2", help="use python2 instead of python3 (default)", action="store_true")
    argparser.add_argument("input", type=str, help="bython files to process", nargs=1)
    argparser.add_argument("args", type=str, help="arguments to script", nargs=argparse.REMAINDER)


    # Parse arguments
    cmd_args = argparser.parse_args()


    # Translate bython to python
    try:
        current_file_name = cmd_args.input[0]
        parser.parse_file(cmd_args.input[0], cmd_args.lower_true)

        if cmd_args.multiple:
            for arg in cmd_args.args:
                current_file_name = arg
                parser.parse_file(arg, cmd_args.lower_true)

    except (TypeError, FileNotFoundError):
        print("Error while parsing file", current_file_name)
        return


    # Stop if we were only asked to translate
    if cmd_args.compile:
        return


    # Run file
    if cmd_args.python2:
        python_command = "python"
    else:
        python_command = "python3"

    os.system("%s %s %s" % (python_command, parser._change_file_name(cmd_args.input[0]), " ".join(i for i in cmd_args.args)))


    # Delete file if requested
    if not cmd_args.keep:
        os.remove(parser._change_file_name(cmd_args.input[0]))


if __name__ == '__main__':
    main()


