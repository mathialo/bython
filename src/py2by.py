#! /usr/bin/python3
import os
import re
import argparse
import sys


def parse_indent_style_input(indentinput):
    if indentinput == "1s":
        return " "

    elif indentinput == "2s":
        return "  "

    elif indentinput == "4s":
        return "    "

    elif indentinput == "8s":
        return "        "

    elif indentinput == "t":
        return "\t"

    else:
        return None


def ends_in_py(word):
    return word[-3:] == ".py"


def change_file_name(name):
    if ends_in_py(name):
        return name[:-3] + ".by"

    else:
        return name + ".by"


def reverse_parse(filename, indent_style):
    indent_symbol = parse_indent_style_input(indent_style)

    if not indent_symbol:
        print("Input error: %s is not a valid indentation style!" % (indent_style))
        sys.exit(1)

    infile = open(filename, "r")
    outfile = open(change_file_name(filename), "w")

    previous_line = ""
    indentation_level = 0

    for line in infile:
        pass

    infile.close()
    outfile.close()


def main():
    argparser = argparse.ArgumentParser("py2by", description="py2by translates python to bython", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("input", type=str, help="python file to translate", nargs=1)
    argparser.add_argument("-i", "--indent_style", type=str, help="style of indentation to look for: 1s, 2s, 4s, 8s or t (default: 4s)", nargs=1)

    cmd_args = argparser.parse_args()

    reverse_parse(cmd_args.input, cmd_args.indent_style[0])


if __name__ == '__main__':
    main()