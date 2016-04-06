#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define true 1
#define false 0
typedef char bool;

bool ends_in_by(char *str);



int main(int argc, char const *argv[]) {
	
	bool compile_only = false;
	unsigned int filename_position = 1;

	if (argc <= 1) {
		printf("No arguments! For help run \"bython -h\"\n");
		return 0;
	}

	if (strcmp(argv[1], "-h") == 0) {
		printf("Bython is a python preprosessor that translates braces into indentation\n");
		printf("Proper use:\n\n");
		printf("       bython <opt: flags> [filename] <opt: cmd-args>\n\n");
		printf("Available flags:\n");
		printf("    -h   Help. Displays this message\n");
		printf("    -v   Version. Displays whivh version of bython you have installed\n");
		printf("    -c   Compile only. Does not run the generated python file.\n");
		printf("    -a   Compile all .by-files in directory (useful for when you're importing)\n");
		return 0;
	}

	if (strcmp(argv[1], "-v") == 0) {
		printf("Bython v. 0.1a pre-alpha\n");
		return 0;
	}

	if (strcmp(argv[1], "-c") == 0) {
		compile_only = true;
		filename_position++;
	}

	char *proccmd = malloc(256*sizeof(char));

	strcat(proccmd, "python /home/mathias/prog/bython/bython.py ");
	strcat(proccmd, argv[filename_position]);

	int returnVal = system(proccmd);

	if (returnVal != 0) {
		printf("Bython error: Something went wrong durnig parsing!\n");
		return -1;
	}

	if (compile_only) {
		return 0;
	}

	char *runcmd = malloc(256*sizeof(char));

	strcat(runcmd, "python bython_out.py");

	int i;
	for (i=2; i<argc; i++) {
		strcat(runcmd, " ");
		strcat(runcmd, argv[i]);
	}

	system(runcmd);

	system("rm bython_out.py");

	return 0;
}
