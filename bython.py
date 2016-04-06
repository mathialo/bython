import sys

def ends_in_by(word):
	return word[-3:] == ".by"

def change_file_name(name):
	if ends_in_by(name):
		return name[:-3] + ".py"
	else:
		return name + ".py"

def parse_file(filename):
	infile = open(filename, 'r')
	outfile = open(change_file_name(filename), 'w')

	indentation_level = 0
	indentation_sign = "    "

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

		# convert back to string and write line to file
		line_string = ''.join(line_list)
		outfile.write(line_string.rstrip() + "\n")

def main():
	for i in range(len(sys.argv)):
		if i==0: continue

		parse_file(sys.argv[i]	)

if __name__ == '__main__':
	main()
