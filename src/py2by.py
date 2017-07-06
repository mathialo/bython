#! /usr/bin/python3
import os
import re
import argparse
import sys


def parse_indent_style_input(indentinput):
    if not indentinput:
        return "    "

    elif indentinput[0] == "1s":
        return " "

    elif indentinput[0] == "2s":
        return "  "

    elif indentinput[0] == "4s":
        return "    "

    elif indentinput[0] == "8s":
        return "        "

    elif indentinput[0] == "t":
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


def count_indent_level(whitespace, indent_symbol):

    new_whitespace, numsubs = re.subn(indent_symbol, "", whitespace)

    if not new_whitespace == "":
        # Not all whitespace was consumed => illigal indentation
        return -1

    else:
        return numsubs



def reverse_parse(filename, indent_style):
    indent_symbol = parse_indent_style_input(indent_style)

    if not indent_symbol:
        print("Input error: %s is not a valid indentation style!" % (indent_style))
        sys.exit(1)

    infile = open(filename, "r")
    outfile = open(change_file_name(filename), "w")

    previous_line = ""
    indentation_level = 0

    i = 1
    for line in infile:
        if line in ("\n", "\n\r", "\r\n"):
            leading_whitespace = ""
        else:
            leading_whitespace = line.split(line.lstrip())[0]

        print("%d: %d" % (i, count_indent_level(leading_whitespace, indent_symbol)))
        i += 1

    infile.close()
    outfile.close()


def main():
    argparser = argparse.ArgumentParser("py2by", description="py2by translates python to bython", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("input", type=str, help="python file to translate", nargs=1)
    argparser.add_argument("-i", "--indent_style", type=str, help="style of indentation to look for: 1s, 2s, 4s, 8s or t (default: 4s)", nargs=1)

    cmd_args = argparser.parse_args()

    reverse_parse(cmd_args.input[0], cmd_args.indent_style)


if __name__ == '__main__':
    main()