#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef enum { LOAD, STORE, LOAD_ADDR, ADD, SUB } InstructionType;

typedef struct {
    InstructionType type;
    char op1[32]; // Increased size to handle longer identifiers
    char op2[32];
    char op3[32];
} Instruction;

typedef struct {
    Instruction *code;
    int size;
    int regCount;
} CodeGenerator;

void initGenerator(CodeGenerator *gen) {
    gen->code = NULL;
    gen->size = 0;
    gen->regCount = 0;
}

void addInstruction(CodeGenerator *gen, InstructionType type, const char *op1, const char *op2, const char *op3) {
    gen->code = realloc(gen->code, (gen->size + 1) * sizeof(Instruction));
    if (!gen->code) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    gen->code[gen->size].type = type;
    strncpy(gen->code[gen->size].op1, op1 ? op1 : "", 31);
    gen->code[gen->size].op1[31] = '\0'; // Ensure null-termination
    strncpy(gen->code[gen->size].op2, op2 ? op2 : "", 31);
    gen->code[gen->size].op2[31] = '\0';
    strncpy(gen->code[gen->size].op3, op3 ? op3 : "", 31);
    gen->code[gen->size].op3[31] = '\0';
    gen->size++;
}

char* newReg(CodeGenerator *gen) {
    char *reg = malloc(10 * sizeof(char)); // Dynamically allocate memory
    if (!reg) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }
    snprintf(reg, 10, "r%d", gen->regCount++);
    return reg;
}

// Returns the name of the register or variable
char* generateRvalue(CodeGenerator *gen, const char *x) {
    if (!x) return NULL; // Handle NULL input
    // If x is identifier or constant, return a copy of x
    if (isalpha(x[0]) || isdigit(x[0])) {
        char *result = strdup(x);
        if (!result) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
        return result;
    } else {
        // Otherwise, create a new temp and return its name
        char *temp = newReg(gen);
        addInstruction(gen, LOAD, temp, x, "");
        return temp;
    }
}

// lvalue calls rvalue to generate instruction
char* generateLvalue(CodeGenerator *gen, const char *x) {
    if (!x) return NULL; // Handle NULL input
    char *val = generateRvalue(gen, x);
    char *reg = newReg(gen);
    addInstruction(gen, LOAD_ADDR, reg, val, "");
    free(val); // Free the memory allocated by generateRvalue
    return reg;
}

void generateAssignment(CodeGenerator *gen, const char *var, const char *reg) {
    if (var && reg) {
        addInstruction(gen, STORE, reg, var, "");
    }
}

void generateAdd(CodeGenerator *gen, const char *result, const char *op1, const char *op2) {
    if (result && op1 && op2) {
        addInstruction(gen, ADD, result, op1, op2);
    }
}

void printCode(CodeGenerator *gen) {
    printf("\nGenerated Code:\n");
    for (int i = 0; i < gen->size; i++) {
        switch (gen->code[i].type) {
            case LOAD: printf("LOAD %s, %s\n", gen->code[i].op1, gen->code[i].op2); break;
            case STORE: printf("STORE %s, %s\n", gen->code[i].op1, gen->code[i].op2); break;
            case LOAD_ADDR: printf("LOAD_ADDR %s, %s\n", gen->code[i].op1, gen->code[i].op2); break;
            case ADD: printf("ADD %s, %s, %s\n", gen->code[i].op1, gen->code[i].op2, gen->code[i].op3); break;
            case SUB: printf("SUB %s, %s, %s\n", gen->code[i].op1, gen->code[i].op2, gen->code[i].op3); break;
        }
    }
}

void freeGenerator(CodeGenerator *gen) {
    free(gen->code);
    gen->code = NULL;
    gen->size = 0;
    gen->regCount = 0;
}

int main() {
    CodeGenerator gen;
    initGenerator(&gen);

    // Example: lvalue and rvalue usage
    // lvalue for identifier
    char *lv1 = generateLvalue(&gen, "x");
    printf("lvalue(x) -> %s\n", lv1);
    free(lv1); // Free allocated memory

    // rvalue for identifier
    char *rv1 = generateRvalue(&gen, "y");
    printf("rvalue(y) -> %s\n", rv1);
    free(rv1);

    // rvalue for constant
    char *rv2 = generateRvalue(&gen, "42");
    printf("rvalue(42) -> %s\n", rv2);
    free(rv2);

    // rvalue for expression (not identifier/constant)
    char *rv3 = generateRvalue(&gen, "(y+z)");
    printf("rvalue((y+z)) -> %s\n", rv3);
    free(rv3);

    printCode(&gen);
    freeGenerator(&gen); // Clean up allocated memory
    return 0;
}