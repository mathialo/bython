#! /usr/bin/python3
import os
import re
import argparse
import sys
from tokenize import tokenize, untokenize, tok_name, INDENT, DEDENT, NAME

'''
pyfile = open("simpletest.py","rb")
tokens = list(tokenize(pyfile.readline))

pyfile.close()

for token in tokens:
    print(token.start[0], tok_name[token.exact_type],token.exact_type,token.string)
'''

def ends_in_py(word):
    return word[-3:] == ".py"


def change_file_name(name):
    if ends_in_py(name):
        return name[:-3] + ".by"
    else:
        return name + ".by"


def reverse_parse(filename):
    infile = open(filename, "rb")
    
    inlines = infile.readlines()
    for index, line in enumerate(inlines):
        inlines[index] = line.decode("utf-8")
        inlines[index] = inlines[index].rstrip()
    infile.seek(0)
    tokens = list(tokenize(infile.readline))
    infile.close()
    
    # Stores a list of tuples for INDENT/DEDENT
    # (token, line number, position in line)
    indent_tracker = []
    
    # Using indent_levels as stack to keep track of the brace positions
    # populate indent_tracker
    indent_levels = []
    position = 0;
    line_of_last_name_token = 0;
    for token in tokens:
        current_line = token.start[0]
        if ((token.exact_type == NAME)
            and line_of_last_name_token != current_line):
            line_of_last_name_token = current_line
            position = token.start[1]
        if (token.exact_type == INDENT):
            indent_levels.append(position)
            indent_tracker.append((INDENT,current_line,position))
        if (token.exact_type == DEDENT):
            indent_tracker.append((DEDENT,current_line,indent_levels.pop()))
            
    # We need to know how many extra lines have been added,
    # to adjust line numbers recorded in indent_tracker
    extra = 0
    
    for indent in indent_tracker:
        token = indent[0]
        index = indent[1]
        position = indent[2]
        print(indent)
        inlines.insert(
            index + extra - 1,
            " " * position
            + ("}","{")[token==INDENT]
        )
        extra += 1

    for line in inlines:
        print(line)


def main():
    argparser = argparse.ArgumentParser("py2by", description="py2by translates python to bython", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v", "--version", action="version", version="py2by is a part of Bython v0.3\nMathias Lohne 2017")
    argparser.add_argument("input", type=str, help="python file to translate", nargs=1)

    cmd_args = argparser.parse_args()

    try:
        reverse_parse(cmd_args.input[0])

    except RuntimeError as e:
        print("Error: %s" % str(e) , file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
