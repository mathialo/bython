#define VERSON_NUMBER "0.2"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define true 1
#define false 0
typedef char bool;

bool ends_in_by(const char *word);
void change_file_name(const char *previous_name, char **new_name);
void print_help();
void print_version();
void print_error(int error_number, const char *add_msg);
bool parse_flags(const char *flags, bool *compile_only, bool *remove_files, bool *add_true_line);
bool get_install_directory(char *install_location);

int main(int argc, char const *argv[]) {
	int i;
	char *new_name;
	bool cont;
	bool compile_only, remove_files, add_true_line;
	unsigned int filename_position = 1;
	char *proccmd, *runcmd;
	int return_val;

	char *install_location = malloc(256*sizeof(char));
	get_install_directory(install_location);

	/* Run files by default, remove files by default */
	compile_only = false;
	remove_files = true;

	/* Print args for debug */
	/*for (i=0; i<argc; i++) {
		printf("%s\n", argv[i]);
	}*/

	/* No args, quit program */
	if (argc <= 1) {
		print_error(0, NULL);
		return -1;
	}

	/* check for flags, and act accordingly */
	if (argv[1][0] == '-') {
		cont = parse_flags(argv[1], &compile_only, &remove_files, &add_true_line);
		filename_position++;

		/* Exit if we aren't supposed to continue (ie. if we for ex. printed help) */
		if (!cont) {
			return 0;
		}

		/* We must now update where the file is, and check if we have enough args */
		if (argc <= 2) {
			print_error(0, NULL);
			return -1;
		}
	}

	/* Process bython-files. Check if file exists. Exit if it doesn't */
	for (i=filename_position; i<argc; i++) {
		if (access(argv[i], R_OK) == -1) {
			print_error(2, argv[i]);
			return -1;
		}
	}

	/* Construct command */
	proccmd = malloc(256*sizeof(char));

	strcat(proccmd, "python ");
	strcat(proccmd, install_location);
	strcat(proccmd, "/bython.py");

	if (add_true_line) strcat(proccmd, " ADD_TRUE_LINE");

	for (i=filename_position; i<argc; i++) {
		strcat(proccmd, " ");
		strcat(proccmd, argv[i]);
	}

	/* Run command: */
	return_val = system(proccmd);

	/* Check for errors during compilation. Exit if there are any */
	if (return_val != 0) {
		print_error(1, NULL);
		return -1;
	}

	/* If the user asked to not run the files, we will stop now. */
	if (compile_only) {
		return 0;
	}

	/* Run python-file. Construct command. Change source.by to source.py */
	change_file_name(argv[filename_position], &new_name);

	runcmd = malloc(256*sizeof(char));
	strcat(runcmd, "python ");
	strcat(runcmd, new_name);

	/* cmd-args. deprecated due to compilation of multiple files */
	/*for (i=2; i<argc; i++) {
		strcat(runcmd, " ");
		strcat(runcmd, argv[i]);
	}*/

	system(runcmd);

	if (remove_files) {
		for (i=filename_position; i<argc; i++) {
			free(new_name);
			change_file_name(argv[i], &new_name);
			remove(new_name);
		}
	}

	return 0;
}

/* This funciton is platform specific for Linux. Remake to create a windows/mac version. */
bool get_install_directory(char *install_location) {
	char* path_end;

	if (readlink ("/proc/self/exe", install_location, 256) <= 0)
		return false;

	path_end = strrchr(install_location, '/');

	if (path_end == NULL)
		return false;

 	path_end++;
 	/* Obtain the directory containing the program by truncating the
	path after the last slash.  */
	*path_end = '\0';
	return true;
}


bool parse_flags(const char *flags, bool *compile_only, bool *remove_files, bool *add_true_line) {
	int num_of_flags, i;
	bool result = false;

	num_of_flags = strlen(flags)-1;


	for (i=1; i<num_of_flags+1; i++) {
		switch (flags[i]) {
			case 'c':
				*compile_only = true;
				result = true;
				break;

			case 'h':
				print_help();
				break;

			case 'v':
				print_version();
				break;

			case 'k':
				*remove_files = false;
				result = true;
				break;

			case 't':
				*add_true_line = true;
				result = true;
				break;

			default:
				printf("Bython error: Unknown flag: %c\n", flags[i]);
				exit(-1);
				break;

		}
	}

	return result;
}

void print_error(int error_number, const char *add_msg) {
	switch (error_number) {
		case 0:
			printf("Bython error: No input files! For help, type \"bython -h\"\n");
			break;

		case 1:
			printf("Bython error: Something went wrong durnig parsing!\n");
			break;

		case 2:
			printf("Bython error: Cannot find file: %s\n", add_msg);
			break;

	}
}

void print_help() {
	printf("Bython is a python preprosessor that translates braces into indentation\n");
	printf("Proper use:\n\n");
	printf("       bython <opt: flags> [filename] <opt: more files>\n\n");
	printf("Available flags:\n");
	printf("    -h   Help. Displays this message\n");
	printf("    -v   Version. Displays whivh version of bython you have installed\n");
	printf("    -c   Compile only. Does not run the generated python file.\n");
	printf("    -k   Keep all the generated python files\n");
	printf("    -t   Adds support for lower case true/false\n");
}


void print_version() {
	printf("Bython v%s\n", VERSON_NUMBER);
	printf("Mathias Lohne, 2016\n");
}


bool ends_in_by(const char *word) {
	char *tmp = malloc(4*sizeof(char));
	int len = strlen(word);
	bool result;

	strncpy(tmp, word + len-3, 3);
	tmp[4] = '\0';

	result = strcmp(tmp, ".by") == 0;
	free(tmp);

	return result;
}

void change_file_name(const char *previous_name, char **new_name) {
	int len = (int)strlen(previous_name);

	if (ends_in_by(previous_name)) {
		*new_name = malloc(len*sizeof(char));
		memcpy(*new_name, previous_name, len);
		(*new_name)[len-2] = 'p';

	} else {
		*new_name = malloc((len + 3)*sizeof(char));
		strcat(*new_name, previous_name);
		strcat(*new_name, ".py");
	}
}
