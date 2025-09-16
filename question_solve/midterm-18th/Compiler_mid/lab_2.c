
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

const char *input;
int pos = 0;

void error(const char *msg) {
	printf("Error: %s at '%c'\n", msg, input[pos]);
	exit(1);
}

void term() {
	if (isdigit(input[pos])) {
		printf("Matched digit: %c\n", input[pos]);
		pos++;
	} else {
		error("Expected digit");
	}
}

void rest() {
	while (input[pos] == '+') {
		printf("Matched '+'\n");
		pos++;
		term();
	}
	// epsilon: do nothing
}

void expr() {
	term();
	rest();
}

int main() {
	char buf[100];
	printf("Enter input (digits and '+'): ");
	fgets(buf, 100, stdin);
	buf[strcspn(buf, "\n")] = 0;
	input = buf;
	pos = 0;
	expr();
	if (input[pos] == '\0') {
		printf("Parsing successful.\n");
	} else {
		printf("Parsing failed at '%c'.\n", input[pos]);
	}
	return 0;
}
