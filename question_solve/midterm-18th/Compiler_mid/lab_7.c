#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Symbol {
    char name[50];
    char type[20];
    int line;
    struct Symbol *next;
} Symbol;

typedef struct Scope {
    char name[20];
    Symbol *symbols;
    struct Scope *parent;
    struct Scope *child;
} Scope;

typedef struct {
    Scope *global;
    Scope *current;
} ChainedTable;

void initTable(ChainedTable *table) {
    table->global = (Scope*)malloc(sizeof(Scope));
    strcpy(table->global->name, "global");
    table->global->symbols = NULL;
    table->global->parent = NULL;
    table->global->child = NULL;
    table->current = table->global;
}

void enterScope(ChainedTable *table, char *name) {
    Scope *new = (Scope*)malloc(sizeof(Scope));
    strcpy(new->name, name);
    new->symbols = NULL;
    new->parent = table->current;
    new->child = NULL;
    
    if(table->current->child == NULL) {
        table->current->child = new;
    } else {
        Scope *sibling = table->current->child;
        while(sibling->child != NULL) {
            sibling = sibling->child;
        }
        sibling->child = new;
    }
    
    table->current = new;
}

void exitScope(ChainedTable *table) {
    if(table->current->parent != NULL) {
        table->current = table->current->parent;
    }
}

void insert(ChainedTable *table, char *name, char *type, int line) {
    Symbol *new = (Symbol*)malloc(sizeof(Symbol));
    strcpy(new->name, name);
    strcpy(new->type, type);
    new->line = line;
    new->next = table->current->symbols;
    table->current->symbols = new;
}

Symbol* lookup(ChainedTable *table, char *name) {
    Scope *scope = table->current;
    while(scope != NULL) {
        Symbol *sym = scope->symbols;
        while(sym != NULL) {
            if(strcmp(sym->name, name) == 0) {
                return sym;
            }
            sym = sym->next;
        }
        scope = scope->parent;
    }
    return NULL;
}

void printScope(Scope *scope, int indent) {
    for(int i = 0; i < indent; i++) printf("  ");
    printf("Scope: %s\n", scope->name);
    
    for(int i = 0; i < indent; i++) printf("  ");
    printf("%-15s %-15s %-10s\n", "Name", "Type", "Line");
    
    Symbol *sym = scope->symbols;
    while(sym != NULL) {
        for(int i = 0; i < indent; i++) printf("  ");
        printf("%-15s %-15s %-10d\n", sym->name, sym->type, sym->line);
        sym = sym->next;
    }
    
    if(scope->child != NULL) {
        printScope(scope->child, indent + 1);
    }
}

void printTable(ChainedTable *table) {
    printScope(table->global, 0);
}

int main() {
    ChainedTable table;
    initTable(&table);
    
    insert(&table, "x", "int", 10);
    insert(&table, "y", "float", 12);
    
    enterScope(&table, "func1");
    insert(&table, "a", "int", 20);
    insert(&table, "b", "char", 22);
    
    enterScope(&table, "loop");
    insert(&table, "i", "int", 30);
    
    printTable(&table);
    
    Symbol *sym = lookup(&table, "x");
    if(sym) {
        printf("\nFound: %s (type: %s, line: %d)\n", sym->name, sym->type, sym->line);
    }
    
    return 0;
}