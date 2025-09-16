
#include <stdio.h>
#include <ctype.h>
#define MAX 100

char stack[MAX];
int top = -1;

void push(char c) { stack[++top] = c; }
char pop() { return stack[top--]; }
char peek() { return top >= 0 ? stack[top] : '\0'; }

int precedence(char op) {
	if (op == '+' || op == '-') return 1;
	if (op == '*' || op == '/') return 2;
	return 0;
}

void infixToPostfix(const char *expr) {
	for (int i = 0; expr[i]; i++) {
		char c = expr[i];
		if (isspace(c)) continue;
		if (isalnum(c)) {
			printf("%c", c);
		} else if (c == '(') {
			push(c);
		} else if (c == ')') {
			while (peek() != '(' && top != -1) printf("%c", pop());
			if (peek() == '(') pop();
		} else if (c == '+' || c == '-' || c == '*' || c == '/') {
			while (top != -1 && precedence(peek()) >= precedence(c)) printf("%c", pop());
			push(c);
		}
	}
	while (top != -1) printf("%c", pop());
	printf("\n");
}

int main() {
	char expr[MAX];
	printf("Enter infix expression: ");
	fgets(expr, MAX, stdin);
	expr[strcspn(expr, "\n")] = 0;
	infixToPostfix(expr);
	return 0;
}
