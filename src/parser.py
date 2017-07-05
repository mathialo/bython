import re


def _ends_in_by(word):
    return word[-3:] == ".by"


def _change_file_name(name):
    if _ends_in_by(name):
        return name[:-3] + ".py"

    else:
        return name + ".py"


def parse_file(filename, add_true_line):
    infile = open(filename, 'r')
    outfile = open(_change_file_name(filename), 'w')

    indentation_level = 0
    indentation_sign = "    "

    if add_true_line:
        outfile.write("true=True; false=False;\n")

    # Read file to string
    infile_str_raw = ""
    for line in infile:
        infile_str_raw += line


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


    print(infile_str_indented)

    infile.close()
    outfile.close()
