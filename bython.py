import sys, os

infile = open(sys.argv[1], 'r')
outfile = open('bython_out.py', 'w')

infile_string = infile.read();
infile_list = list(infile_string)

for i in range(len(infile_list)):
	if (infile_list[i] == "{"):
		infile_list[i] = ":"

	if (infile_list[i] == "}"):
		infile_list[i] = " "


infile_string = ''.join(infile_list)
outfile.write(infile_string)
