#include <stdio.h>


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

	return 0;
}
