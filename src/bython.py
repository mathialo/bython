#! /usr/bin/python3
import parser
import argparse

def ends_in_by(word):
    return word[-3:] == ".by"


def change_file_name(name):
    if ends_in_by(name):
        return name[:-3] + ".py"
    else:
        return name + ".py"

def main():
	# Setup argument parser
    argparser = argparse.ArgumentParser("bython", description="Bython is a python preprosessor that translates braces into indentation", formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument("-v", "--version", action="version", version="Bython v0.3\nMathias Lohne 2017")
    argparser.add_argument("-c", "--compile", help="Compile only (don't run files)", action="store_true")
    argparser.add_argument("-m", "--multiple", help="Treat arguments as additional files to process", action="store_true")
    argparser.add_argument("-k", "--keep", help="Keep generated python files", action="store_true")
    argparser.add_argument("-t", "--lower_true", help="Adds support for lower case true/false", action="store_true")
    argparser.add_argument("-2", "--python2", help="Use python2 instead of python3 (default)", action="store_true")
    argparser.add_argument("input", type=str, help="bython files to process", nargs=1)
    argparser.add_argument("args", type=str, help="arguments to script", nargs=argparse.REMAINDER)

    # Parse arguments
    cmd_args = argparser.parse_args()

    # for i in range(len(sys.argv)):
    #     if i==0: continue

    #     if i==1 and sys.argv[i] == "ADD_TRUE_LINE":
    #         add_true_line = True
    #         continue

    #     parse_file(sys.argv[i], add_true_line)

if __name__ == '__main__':
	main()


