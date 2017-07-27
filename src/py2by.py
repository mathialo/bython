#! /usr/bin/python3
import os
import re
import argparse
import sys

""" Translates python to bython

This program translates python files and outputs a bython (.by) file. Used
with the bython application.

Example invocation:

    py2by legacycode.py -i 8s

    Outputs legacycode.by in the working directory.

#TODO: Finish this
"""

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
        raise RuntimeError("Illegal indentation detected.\nMaybe the selected indentation style is wrong?")

    else:
        return numsubs



def reverse_parse(filename, indent_style):
    indent_symbol = parse_indent_style_input(indent_style)

    if not indent_symbol:
        raise RuntimeError("%s is not a valid indentation style!" % (indent_style))

    infile = open(filename, "r")
    outfile = open(change_file_name(filename), "w")

    last_line = ""
    last_level = 0

    num_open = 0
    num_close = 0

    level = 0

    for line in infile:
        if not line.strip() == "":
            if line in ("\n", "\n\r", "\r\n"):
                leading_whitespace = ""

            else:
                leading_whitespace = line.split(line.lstrip())[0]

            level = count_indent_level(leading_whitespace, indent_symbol)


        new_last, num_subs = re.subn(r"\s*:$", " {", last_line)
        num_open += num_subs
        outfile.write(new_last)

        if level < last_level:
            decrese = last_level - level
            for i in range(decrese):
                outfile.write((level + decrese - i -1)*indent_symbol + "}\n")
                num_close += 1

        last_line = line
        last_level = level


    outfile.write(last_line)

    if last_level > 0:
        outfile.write("\n")
        decrese = last_level
        for i in range(decrese):
            outfile.write((decrese - i - 1)*indent_symbol + "}\n")
            num_close += 1



    if num_open > num_close:
        outfile.write("}\n")
        num_close += 1

    if (num_open != num_close):
        raise RuntimeError("Unmatching number of braces created.")

    infile.close()
    outfile.close()


def main():
    argparser = argparse.ArgumentParser("py2by", description="py2by translates python to bython", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v", "--version", action="version", version="py2by is a part of Bython v0.3\nMathias Lohne 2017")
    argparser.add_argument("input", type=str, help="python file to translate", nargs=1)
    argparser.add_argument("-i", "--indent_style", type=str, help="style of indentation to look for: 1s, 2s, 4s, 8s or t (default: 4s)", nargs=1)

    cmd_args = argparser.parse_args()

    try:
        reverse_parse(cmd_args.input[0], cmd_args.indent_style)

    except RuntimeError as e:
        print("Error: %s" % str(e) , file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
