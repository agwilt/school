#include <stdio.h>

int main()
{
	char *input;
	int counter = 0;

	fgets(input, 1000, stdin);

	printf("String: %s\n", input);
	
	z0:
		printf("z0\t%c\n", input[counter]);
		switch (input[counter]) {
			case '\n':
			case '\0': {printf("Can't end here\n"); return 1; }
			case '0': { counter++; goto z0;}
			case '3':
			case '6':
			case '9': { counter++; goto z3;}
			case '1':
			case '4':
			case '7': { counter++; goto z1;}
			case '2':
			case '5':
			case '8': { counter++; goto z2;}
			default: {printf("Invalid letter: %d\n", input[counter]); return 2;}
		}

	z1:
		printf("z1\t%c\n", input[counter]);
		switch (input[counter]) {
			case '\n':
			case '\0': {printf("Can't end here\n"); return 1; }
			case '0':
			case '3':
			case '6':
			case '9': { counter++; goto z1;}
			case '1':
			case '4':
			case '7': { counter++; goto z2;}
			case '2':
			case '5':
			case '8': { counter++; goto z3;}
			default: {printf("Invalid letter: %d\n", input[counter]); return 2;}
		}
	z2:
		printf("z2\t%c\n", input[counter]);
		switch (input[counter]) {
			case '\n':
			case '\0': {printf("Can't end here\n"); return 1; }
			case '0':
			case '3':
			case '6':
			case '9': { counter++; goto z2;}
			case '1':
			case '4':
			case '7': { counter++; goto z3;}
			case '2':
			case '5':
			case '8': { counter++; goto z1;}
			default: {printf("Invalid letter: %d\n", input[counter]); return 2;}
		}

	z3:
		printf("z3\t%c\n", input[counter]);
		switch (input[counter]) {
			case '\n':
			case '\0': {printf("valid!\n"); return 0;}
			case '2':
			case '5':
			case '8': {counter++; goto z2;}
			case '1':
			case '4':
			case '7': {counter++; goto z1;}
			case '0':
			case '3':
			case '6':
			case '9': {counter++; goto z3;}
			default: {printf("Invalid letter: %d\n", input[counter]); return 2;}
		}

	return 5;
}
