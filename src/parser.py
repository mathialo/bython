
def parse_file(filename, add_true_line):
    infile = open(filename, 'r')
    outfile = open(change_file_name(filename), 'w')

    indentation_level = 0
    indentation_sign = "    "

    if (add_true_line):
        outfile.write("true=True; false=False;\n")

    for line in infile:
        # skip empty lines:
        if line in ('\n', '\r\n'):
            outfile.write(line)
            continue

        # remove existing whitespace:
        line = line.lstrip()

        # add new whitespace:
        for i in range(indentation_level):
            line = indentation_sign + line
        
        # remove brackets and update indentation level
        line_list = list(line)

        for i in range(len(line_list)):
            if (line_list[i] == "{"):
                line_list[i] = ":"
                indentation_level += 1

            if (line_list[i] == "}"):
                line_list[i] = " "
                indentation_level -= 1

            if (line_list[i] == ";"):
                line_list[i] = " "

        # convert from list of chars to string
        line_string = ''.join(line_list)

        # write to file
        outfile.write(line_string.rstrip() + "\n")

    infile.close()
    outfile.close()
