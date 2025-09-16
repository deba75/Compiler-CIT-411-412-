#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX 100

typedef struct {
    char items[MAX];
    int top;
} Stack;

void push(Stack *s, char c) {
    s->items[++s->top] = c;
}

char pop(Stack *s) {
    return s->items[s->top--];
}

char peek(Stack *s) {
    return s->items[s->top];
}

int isEmpty(Stack *s) {
    return s->top == -1;
}

// Simple predictive parser for grammar: E -> TE' | +TE' | ε, E' -> *TE' | ε, T -> FT' | FT', T' -> +FT' | ε, F -> (E) | id
void predictiveParser(char *input) {
    Stack stack;
    stack.top = -1;
    push(&stack, '$');
    push(&stack, 'E');
    
    int i = 0;
    while (!isEmpty(&stack)) {
        char top = peek(&stack);
        char current = input[i];
        
        if (top == current) {
            pop(&stack);
            i++;
        } 
        else if (top == 'E') {
            pop(&stack);
            if (current == 'i' || current == '(') {
                push(&stack, 'A');  // E'
                push(&stack, 'T');
            } else {
                printf("Error at %c\n", current);
                return;
            }
        }
        else if (top == 'A') {  // E'
            pop(&stack);
            if (current == '+') {
                push(&stack, 'A');
                push(&stack, 'T');
                push(&stack, '+');
            }
        }
        else if (top == 'T') {
            pop(&stack);
            if (current == 'i' || current == '(') {
                push(&stack, 'B');  // T'
                push(&stack, 'F');
            } else {
                printf("Error at %c\n", current);
                return;
            }
        }
        else if (top == 'B') {  // T'
            pop(&stack);
            if (current == '*') {
                push(&stack, 'B');
                push(&stack, 'F');
                push(&stack, '*');
            }
        }
        else if (top == 'F') {
            pop(&stack);
            if (current == 'i') {
                push(&stack, 'i');
            } else if (current == '(') {
                push(&stack, ')');
                push(&stack, 'E');
                push(&stack, '(');
            } else {
                printf("Error at %c\n", current);
                return;
            }
        }
        else {
            printf("Error: Unexpected symbol %c\n", top);
            return;
        }
    }
    
    if (input[i] == '$') {
        printf("String accepted\n");
    } else {
        printf("String rejected\n");
    }
}

int main() {
    char input[MAX];
    printf("Enter input (end with $): ");
    scanf("%s", input);
    predictiveParser(input);
    return 0;
}