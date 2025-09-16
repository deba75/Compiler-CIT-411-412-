

#include <stdio.h>
#include <string.h>
#include <ctype.h>

const char *keywords[] = {"if", "else", "for", "while", "int", "float", "return", "void"};
int num_keywords = sizeof(keywords)/sizeof(keywords[0]);

int isKeyword(const char *str) {
	for (int i = 0; i < num_keywords; i++) {
		if (strcmp(str, keywords[i]) == 0) return 1;
	}
	return 0;
}

int isIdentifier(const char *str) {
	if (!isalpha(str[0]) && str[0] != '_') return 0;
	for (int i = 1; str[i]; i++) {
		if (!isalnum(str[i]) && str[i] != '_') return 0;
	}
	return 1;
}

int main() {
	char word[100];
	printf("Enter word: ");
	scanf("%99s", word);
	if (isKeyword(word)) printf("%s is a keyword\n", word);
	else if (isIdentifier(word)) printf("%s is an identifier\n", word);
	else printf("%s invalid identifier\n", word);
	return 0;
}
