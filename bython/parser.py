import re
import os

"""
Python module for converting bython code to python code.
"""

def _ends_in_by(word):
    """
    Returns True if word ends in .by, else False

    Args:
        word (str):     Filename to check

    Returns:
        boolean: Whether 'word' ends with 'by' or not
    """
    return word[-3:] == ".by"


def _change_file_name(name, outputname=None):
    """
    Changes *.by filenames to *.py filenames. If filename does not end in .by, 
    it adds .py to the end.

    Args:
        name (str):         Filename to edit
        outputname (str):   Optional. Overrides result of function.

    Returns:
        str: Resulting filename with *.py at the end (unless 'outputname' is
        specified, then that is returned).
    """

    # If outputname is specified, return that
    if outputname is not None:
        return outputname

    # Otherwise, create a new name
    if _ends_in_by(name):
        return name[:-3] + ".py"

    else:
        return name + ".py"


def parse_imports(filename):
    """
    Reads the file, and scans for imports. Returns all the assumed filename
    of all the imported modules (ie, module name appended with ".by")

    Args:
        filename (str):     Path to file

    Returns:
        list of str: All imported modules, suffixed with '.by'. Ie, the name
        the imported files must have if they are bython files.
    """
    infile = open(filename, 'r')
    infile_str = ""

    for line in infile:
        infile_str += line


    imports = re.findall(r"(?<=import\s)[\w.]+(?=;|\s|$)", infile_str)
    imports2 = re.findall(r"(?<=from\s)[\w.]+(?=\s+import)", infile_str)

    imports_with_suffixes = [im + ".by" for im in imports + imports2]

    return imports_with_suffixes


def parse_file(filepath, add_true_line, filename_prefix, outputname=None, change_imports=None):
    """
    Converts a bython file to a python file and writes it to disk.

    Args:
        filename (str):             Path to the bython file you want to parse.
        add_true_line (boolean):    Whether to add a line at the top of the
                                    file, adding support for C-style true/false
                                    in addition to capitalized True/False.
        filename_prefix (str):      Prefix to resulting file name (if -c or -k
                                    is not present, then the files are prefixed
                                    with a '.').
        outputname (str):           Optional. Override name of output file. If
                                    omitted it defaults to substituting '.by' to
                                    '.py'    
        change_imports (dict):      Names of imported bython modules, and their 
                                    python alternative.
    """
    filename = os.path.basename(filepath)
    filedir = os.path.dirname(filepath)

    infile = open(filepath, 'r')
    outfile = open(filename_prefix + _change_file_name(filename, outputname), 'w')

    indentation_level = 0
    indentation_sign = "    "

    if add_true_line:
        outfile.write("true=True; false=False;\n")

    # Read file to string
    infile_str_raw = ""
    for line in infile:
        infile_str_raw += line

    # Add 'pass' where there is only a {}. 
    # 
    # DEPRECATED FOR NOW. This way of doing
    # it is causing a lot of problems with {} in comments. The feature is removed
    # until I find another way to do it. 
    
    # infile_str_raw = re.sub(r"{[\s\n\r]*}", "{\npass\n}", infile_str_raw)

    # Fix indentation
    infile_str_indented = ""
    for line in infile_str_raw.split("\n"):
        # Search for comments, and remove for now. Re-add them before writing to
        # result string
        m = re.search(r"[ \t]*([(\/\/)#].*$)", line)

        # Make sure # sign is not inside quotations. Delete match object if it is
        if m is not None:
            m2 = re.search(r"[\"'].*[(\/\/)#].*[\"']", m.group(0))
            if m2 is not None:
                m = None

        if m is not None:
            add_comment = m.group(0)
            line = re.sub(r"[ \t]*([(\/\/)#].*$)", "", line)
        else:
            add_comment = ""
        
        # replace // with #
        add_comment = add_comment.replace("//", "#", 1)

        # skip empty lines:
        if line.strip() in ('\n', '\r\n', ''):
            infile_str_indented += indentation_level*indentation_sign + add_comment.lstrip() + "\n"
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

        # Replace { with : and remove }
        line = re.sub(r"[\t ]*{[ \t]*", ":", line)
        line = re.sub(r"}[ \t]*", "", line)
        line = re.sub(r"\n:", ":", line)

        infile_str_indented += line + add_comment + "\n"


    # Support for extra, non-brace related stuff
    infile_str_indented = re.sub(r"else\s+if", "elif", infile_str_indented)
    infile_str_indented = re.sub(r";[ \t]+\n", "\n", infile_str_indented)

    # Change imported names if necessary
    if change_imports is not None:
        for module in change_imports:
            infile_str_indented = re.sub("(?<=import\\s){}".format(module), "{} as {}".format(change_imports[module], module), infile_str_indented)
            infile_str_indented = re.sub("(?<=from\\s){}(?=\\s+import)".format(module), change_imports[module], infile_str_indented)

    outfile.write(infile_str_indented)

    infile.close()
    outfile.close()


def remove_indentation(code):
    """
    Removes indentation from string

    Args:
        code (str):     The string that will be manipulated
    
    Returns:
        str: A string with the changes applied
    """
    code = re.sub(r"^[ \t]*", "", code, 1)
    code = re.sub(r"\r?\n[ \t]+", "\n", code)
    return code


def prepare_braces(code):
    """
    Moves braces to the optimal position. E.g.: "while x < 10{".
    Removes additional spacing after "}".
    Ensures comments come after the opening braces. E.g. "while x < 10{ // comment".

    Args:
        code (str):     The string that will be manipulated
    
    Returns:
        str: A string with the changes applied
    """

    # TODO fix issue with brace within comments
    # TODO fix removing spaces and tabs from within strings
    code = re.sub(r"[ \t]*(\/\/.*|\#.*)?\r?\n[ \t]*\{", "{ \\1\n", code)
    code = re.sub(r"(?<=\})[ \t]+\n", "\n", code)
    code = re.sub(r"(?<=\})[ \t]+((else|elif))", "\n\\1", code)
    code = re.sub(r"(?<=\n\})([^\n]+?)(?=\n)", "\n\\1", code)
    code = re.sub(r"[ \t]+(?=\{\n)", "", code)
    return code


def remove_semicolons(code):
    """
    Find and removes the semicolons placed at the end of lines

    Args:
        code (str):     The string that will be manipulated
    
    Returns:
        str: A string with the changes applied
    """
    # remove semicolons, but keep any comments
    # TODO fix: if a semicolon is follwed by a comment starter '//' or '#', the semicolon will be removed even inside strings or comments
    code = re.sub(r"[ \t]*;[ \t]*(\/\/.*|\#.*)?\r?(?=\n)", " \\1", code)

    # remove any extra spaces added at the end of lines
    code = re.sub(r"[ \t]\r?\n", "\n", code)
    
    # remove a semicolon placed right before the EOF
    code = re.sub(r";$", "", code)
    return code


def remove_empty_lines(code):
    """
    Find and removes empty lines

    Args:
        code (str):     The string that will be manipulated
    
    Returns:
        str: A string with the changes applied
    """
    code = re.sub(r"\r?\n[ \t]*(\r?\n[ \t]*)+", "\n", code)
    return code


def indent_if_newline(code, outfile, indentation, indentation_str):
    """
    Applies indentation.

    Args:
        code (str):                 The string that will be manipulated
        outfile (file):             The file which will be indented
        indentation (int):          The desired indentation level
        indentation_str (str):      The indentation style (usually spaces or tabs)
    """
    if code == "\n":
        for x in range(indentation):
            outfile.write(indentation_str)


def parse_file_recursively(filepath, add_true_line=False, filename_prefix="", outputname=None, change_imports=None, debug_mode=False):
    """
    Converts a bython file to a python file recursively and writes it to disk.

    Args:
        filename (str):             Path to the bython file you want to parse.
        add_true_line (boolean):    Whether to add a line at the top of the
                                    file, adding support for C-style true/false
                                    in addition to capitalized True/False.
        filename_prefix (str):      Prefix to resulting file name (if -c or -k
                                    is not present, then the files are prefixed
                                    with a '.').
        outputname (str):           Optional. Override name of output file. If
                                    omitted it defaults to substituting '.by' to
                                    '.py'    
        change_imports (dict):      Names of imported bython modules, and their 
                                    python alternative.
        debug_mode (boolean):       Enables debug output (scope detection)
    """
    
    # inner function for parsing recursively
    def recursive_parser(code, position, scope, outfile, indentation, indentation_str="    ", debug_mode=False):
        """
        Recursive inner function for scope detection and for writing the final .py code to disk

        Args:
            code (str):             The string that will be interpreted
            position (int):         Current position on the code string
            scope (str):            Current scope ("", "{", "(", "#", "//"
                                    "/*", "/'", "/"", "=", "={")
            outfile (file)          The output file which will be writen to
            indentation (int):      The current indentation level
            indentation_str (str):  The indentation style (usually spaces or tabs)
            debug_mode (boolean):   Enables debug output (scope detection)

        Returns:
            int: Next position on the string
        """
        # scope equal to "" means it's on global scope
        # scope equal to "{" means it's on a local scope
        # scope equal to "(" means it's inside function parameters or tuples
        if scope == "" or scope == "{" or scope == "(":

            if scope == "":
                if debug_mode:
                    print("g", end="") # for debugging
            else:
                indentation = indentation + 1

            # keep parsing until EOF
            while position < len(code):

                # check for brace opening
                if code[position] == "{":
                    if debug_mode:
                        print("{", end="") # for debugging
                    outfile.write(":")
                    position = recursive_parser(code, position + 1, "{", outfile, indentation, indentation_str, debug_mode)
                    if scope == "":
                        if debug_mode:
                            print("g", end="") # for debugging
                
                # check for parenthesis opening
                if code[position] == "(":
                    if debug_mode:
                        print("(", end="") # for debugging
                    outfile.write(code[position])
                    position = recursive_parser(code, position + 1, "(", outfile, indentation, indentation_str, debug_mode)

                # check for python-style comment
                elif code[position] == "#":
                    outfile.write(code[position])
                    position = recursive_parser(code, position + 1, "#", outfile, indentation, indentation_str, debug_mode)
                
                # check for c and cpp-style comment
                elif code[position] == "/":
                    #if code[position + 1] == "/":
                        #outfile.write("#")
                        #position = recursive_parser(code, position + 2, "//", outfile, indentation, indentation_str, debug_mode)
                    if code[position + 1] == "*":
                        outfile.write("#")
                        outfile.write(code[position:position+2])
                        position = recursive_parser(code, position + 2, "/*", outfile, indentation, indentation_str, debug_mode)
                    else:
                        outfile.write("/")
                        position = position + 1
                
                # check for single-quote string start
                elif code[position] == "\'":
                    outfile.write("\'")
                    position = recursive_parser(code, position + 1, "\'", outfile, indentation, indentation_str, debug_mode)

                # check for double-quote string start
                elif code[position] == "\"":
                    outfile.write("\"")
                    position = recursive_parser(code, position + 1, "\"", outfile, indentation, indentation_str, debug_mode)
                
                # check for equals (for python dicts with braces)
                elif code[position] == "=":
                    outfile.write(code[position])
                    position = recursive_parser(code, position + 1, "=", outfile, indentation, indentation_str, debug_mode)

                # check for brace closing (when not on global)
                elif scope == "{":
                    if code[position] == "}":
                        if debug_mode:
                            print("}", end="")
                        return position + 1
                    else:
                        if code[position] == "\n" and code[position + 1] == "}":
                                pass
                        else:
                            outfile.write(code[position])
                            indent_if_newline(code[position], outfile, indentation, indentation_str)
                        position = position + 1
                
                # check for parenthesis opening
                elif scope == "(":
                    outfile.write(code[position])
                    indent_if_newline(code[position], outfile, indentation, indentation_str)
                    if code[position] == ")":
                        if debug_mode:
                            print(")", end="")
                        return position + 1
                    position = position + 1

                else:
                    outfile.write(code[position])
                    indent_if_newline(code[position], outfile, indentation, indentation_str)
                    position = position + 1

        # scope equal to "#" means it's inside a python style comment
        elif scope == "#":
            if debug_mode:
                print("#", end="") # for debugging
            while position < len(code):
                outfile.write(code[position])
                indent_if_newline(code[position], outfile, indentation, indentation_str)
                if code[position] == "\n":
                    if debug_mode:
                        print("n", end="") # for debugging
                    return position + 1

                else:
                    position = position + 1
        
        # scope equal to "//" means it's inside a c++ style comment
        elif scope == "//":
            if debug_mode:
                print("//", end="") # for debugging
            while position < len(code):
                outfile.write(code[position])
                indent_if_newline(code[position], outfile, indentation, indentation_str)
                if code[position] == "\n":
                    if debug_mode:
                        print("n", end="") # for debugging
                    return position + 1

                else:
                    position = position + 1
        
        # scope equal to "/*" means it's inside a c style comment
        elif scope == "/*":
            if debug_mode:
                print("/*", end="") # for debugging
            while position < len(code):
                outfile.write(code[position])
                indent_if_newline(code[position], outfile, indentation, indentation_str)
                if code[position] == "\n":
                    outfile.write("#")

                # check for c-style comment closing
                if code[position] == "*":
                    if code[position + 1] == "/":
                        if debug_mode:
                            print("*/", end="") # for debugging
                        outfile.write(code[position + 1])
                        return position + 2
                    else:
                        position = position + 1
                
                else:
                    position = position + 1

        # scope equal to "\'" means it's inside a single quote string
        elif scope == "\'":
            if debug_mode:
                print("\'^", end="") # for debugging
            while position < len(code):
                outfile.write(code[position])
                indent_if_newline(code[position], outfile, indentation, indentation_str)
                # check for single-quote string ending
                if code[position] == "\'":
                    # check if its escaped
                    if code[position - 1] != "\\":
                        if debug_mode:
                            print("$\'", end="") # for debugging
                        return position + 1
                    else:
                        position = position + 1

                else:
                    position = position + 1
        
        # scope equal to "\"" means it's inside a double quote string
        elif scope == "\"":
            if debug_mode:
                print("\"^", end="") # for debugging
            while position < len(code):
                outfile.write(code[position])
                indent_if_newline(code[position], outfile, indentation, indentation_str)
                # check for single-quote string ending
                if code[position] == "\"":
                    # check if its escaped
                    if code[position - 1] != "\\":
                        if debug_mode:
                            print("$\'", end="") # for debugging
                        return position + 1
                    else:
                        position = position + 1
                else:
                    position = position + 1
        
        # scope equal to "=" means a possible python dictionary
        elif scope == "=":
            if debug_mode:
                print("=", end="") # for debugging
            while position < len(code):
                # check for dicts
                if code[position] == "{":
                    outfile.write(code[position])
                    indent_if_newline(code[position], outfile, indentation, indentation_str)
                    if debug_mode:
                        print(".dict.", end="") # for debugging
                    return recursive_parser(code, position + 1, "={", outfile, indentation + 1, indentation_str, debug_mode)

                # check for whitespaces/newlines
                elif re.search(r"[\s\n\r]", code[position]):
                    outfile.write(code[position])
                    indent_if_newline(code[position], outfile, indentation, indentation_str)
                    position = position + 1

                # if it gets here, non-dict was found
                else:
                    indent_if_newline(code[position], outfile, indentation, indentation_str)
                    if debug_mode:
                        print("!", end="") # for debugging
                    return position
        
        # scope equal to "={" means it's inside a python dictionary
        elif scope == "={":
            while position < len(code):
                
                if code[position] == "}":
                    outfile.write(code[position])
                    return position + 1

                else:
                    outfile.write(code[position])
                    if code[position + 1] == "}":
                        indent_if_newline(code[position], outfile, indentation - 1, indentation_str)
                    else:
                        indent_if_newline(code[position], outfile, indentation, indentation_str)
                    position = position + 1

        # if scope is invalid an exception will be thrown
        else:
            raise Exception("invalid scope was reached")


    # get filepath/filename
    filename = os.path.basename(filepath)

    # open input file
    infile = open(filepath, 'r')
    infile_str = infile.read()
    infile.close()

    # open output file
    outfile = open(filename_prefix + _change_file_name(filename, outputname), 'w')

    # true=True; false=False;
    if add_true_line:
        outfile.write("true=True\nfalse=False\n")
    
    # remove indentation
    infile_str = remove_indentation(infile_str)

    # rearrange braces
    infile_str = prepare_braces(infile_str)

    # remove empty lines
    infile_str = remove_empty_lines(infile_str)

    # change 'else if' into 'elif'
    infile_str = re.sub(r"else\s+if", "elif", infile_str)

    # remove semicolons
    infile_str = remove_semicolons(infile_str)

    # change imported names (if necessary)
    # TODO testing
    if change_imports is not None:
        for module in change_imports:
            infile_str = re.sub("(?<=import\\s){}".format(module), "{} as {}".format(change_imports[module], module), infile_str)
            infile_str = re.sub("(?<=from\\s){}(?=\\s+import)".format(module), change_imports[module], infile_str)

    # output filtered file (for debugging)
    if debug_mode:
        filtered_file = open(filename + ".filtered", 'w')
        filtered_file.write(infile_str)
        filtered_file.close()
    
    # adding a newline at EOF
    infile_str += "\n"

    # start recursive function
    recursive_parser(infile_str, 0, "", outfile, 0, "    ", debug_mode)

    if debug_mode:
        print("\n", end="")

    # close output file
    outfile.close()