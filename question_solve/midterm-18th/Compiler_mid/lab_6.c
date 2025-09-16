
// --- LAB 6: Complete Lexical Analyzer ---
#include <stdio.h>
#include <ctype.h>
#include <string.h>

const char *keywords[] = {"if", "else", "for", "while", "int", "float", "return", "void"};
int num_keywords = sizeof(keywords)/sizeof(keywords[0]);

int isKeyword(const char *str) {
    for (int i = 0; i < num_keywords; i++) {
        if (strcmp(str, keywords[i]) == 0) return 1;
    }
    return 0;
}

void tokenize(const char *src) {
    int i = 0;
    while (src[i]) {
        if (isspace(src[i])) { i++; continue; }
        if (isalpha(src[i]) || src[i] == '_') {
            char buf[100]; int j = 0;
            while (isalnum(src[i]) || src[i] == '_') buf[j++] = src[i++];
            buf[j] = 0;
            if (isKeyword(buf)) printf("<KEYWORD, %s>\n", buf);
            else printf("<IDENTIFIER, %s>\n", buf);
        } else if (isdigit(src[i])) {
            char buf[100]; int j = 0;
            while (isdigit(src[i])) buf[j++] = src[i++];
            buf[j] = 0;
            printf("<NUMBER, %s>\n", buf);
        } else if (strchr("+-*/=;(){}<>", src[i])) {
            printf("<SYMBOL, %c>\n", src[i]);
            i++;
        } else {
            printf("<UNKNOWN, %c>\n", src[i]);
            i++;
        }
    }
}

int main() {
    char src[1000];
    printf("Enter source code: ");
    fgets(src, 1000, stdin);
    tokenize(src);
    return 0;
}