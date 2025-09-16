
// --- LAB 4: Skip Whitespace from Source Program ---
#include <stdio.h>
#include <ctype.h>
#define MAX 1000

int main() {
	char src[MAX];
	printf("Enter source program: ");
	fgets(src, MAX, stdin);
	printf("Output (no whitespace): ");
	for (int i = 0; src[i]; i++) {
		if (!isspace(src[i])) putchar(src[i]);
	}
	printf("\n");
	return 0;
}
