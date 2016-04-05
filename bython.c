#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	
	if (argc <= 1) {
		printf("No arguments! For help run \"bython -h\"\n");
		return 0;
	}

	if (strcmp(argv[1], "-h") == 0) {
		printf("Bython is a python preprosessor that translates braces into indentation\n");
		printf("Proper use:\n\n");
		printf("       bython [filename]\n\n");
		printf("Available flags:\n");
		printf("    -h   Help. Displays this message\n");
		printf("    -v   Version. Displays whivh version of bython you have installed\n");
		return 0;
	}

	if (strcmp(argv[1], "-v") == 0) {
		printf("Bython v. 0.1a pre-alpha\n");
		return 0;
	}

	char *proccmd = malloc(256*sizeof(char));

	strcat(proccmd, "python /home/mathias/prog/bython/bython.py ");
	strcat(proccmd, argv[1]);

	int returnVal = system(proccmd);

	if (returnVal != 0) {
		printf("Bython error: Something went wrong durnig parsing!\n");
		return -1;
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
