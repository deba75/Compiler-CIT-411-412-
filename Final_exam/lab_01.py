"""
Lab 01: Lexical Analyzer for C Language
Recognizes: Identifiers, Constants, Comments, White space, Tab, Newline, Punctuation, Operators
Example input: int sum = a + b * 10;
"""

import re

def solve_lab_problem():
    print("=" * 60)
    print("LAB 01: LEXICAL ANALYZER FOR C LANGUAGE")
    print("=" * 60)
    

    keywords = {"int", "float", "char", "double", "if", "else", "while", "for", "return", 
                "void", "main", "include", "printf", "scanf", "const", "static"}
    operators = {"=", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||", 
                "++", "--", "+=", "-=", "*=", "/=", "%", "!", "&", "|", "^", "~"}
    punctuation = {";", ",", "(", ")", "{", "}", "[", "]", ".", ":", "?"}
    
    def lexer(statement):
       
        pattern = r'(/\*[\s\S]*?\*/|//.*?$|[A-Za-z_]\w*|\d+\.?\d*|==|!=|<=|>=|\+\+|--|&&|\|\||[+\-*/=<>!&|^~%]|[;,(){}[\].?:]|\s+)'
        tokens = re.findall(pattern, statement, re.MULTILINE)
        
        result = []
        for tok in tokens:
            if not tok.strip():  
                if '\n' in tok:
                    result.append(("\\n", "Newline"))
                elif '\t' in tok:
                    result.append(("\\t", "Tab"))
                elif tok == ' ':
                    result.append(("space", "White space"))
            elif tok.startswith('//') or (tok.startswith('/*') and tok.endswith('*/')):
                result.append((tok, "Comment"))
            elif tok in keywords:
                result.append((tok, "Keyword"))
            elif tok in operators:
                result.append((tok, "Operator"))
            elif tok in punctuation:
                result.append((tok, "Punctuation"))
            elif re.fullmatch(r'\d+', tok):
                result.append((tok, "Integer Constant"))
            elif re.fullmatch(r'\d+\.\d+', tok):
                result.append((tok, "Float Constant"))
            elif re.fullmatch(r'[A-Za-z_]\w*', tok):
                result.append((tok, "Identifier"))
            else:
                result.append((tok, "Invalid"))
        return result

    
   
    print("\nExample Analysis:")
    example = "int sum = a + b * 10;"
    print(f"Input: {example}")
    
    tokens = lexer(example)
    print("\nLexeme\t\tToken Type")
    print("-" * 40)
    for lex, typ in tokens:
        print(f"{lex:<12}\t{typ}")
    

    print("\n" + "=" * 60)
    print("INTERACTIVE MODE:")
    print("Enter C statements to analyze (press Enter with empty input to exit)")
    print("=" * 60)
    
    while True:
        statement = input("\nEnter statement: ").strip()
        if not statement:
            break
            
        output = lexer(statement)
        print("\nLexeme\t\tToken Type")
        print("-" * 40)
        for lex, typ in output:
            print(f"{lex:<12}\t{typ}")
        
        # Summary
        total_tokens = len(output)
        print(f"\nTotal tokens: {total_tokens}")
    
    print("Analysis complete!")

if __name__ == "__main__":
    solve_lab_problem()

