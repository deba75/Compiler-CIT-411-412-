import re

# Define token categories
keywords = {"int", "float", "if", "else", "while", "for", "return"}
operators = {"=", "+", "-", "*", "/", "==", "!="}
separators = {";", ",", "(", ")", "{", "}"}

def lexer(statement):
    # Regex: match identifiers, numbers, operators, separators, or invalid chunks
    tokens = re.findall(r'[A-Za-z_]\w*|\d+|==|!=|=|\+|\-|\*|/|;|,|\(|\)|\{|\}|\S+', statement)
    
    result = []
    for tok in tokens:
        if tok in keywords:
            result.append((tok, "Keyword"))
        elif tok in operators:
            result.append((tok, "Operator"))
        elif tok in separators:
            result.append((tok, "Separator"))
        elif re.fullmatch(r'\d+', tok):
            result.append((tok, "Number"))
        elif re.fullmatch(r'[A-Za-z_]\w*', tok):
            result.append((tok, "Identifier"))
        else:
            result.append((tok, "Invalid"))
    return result


# -------- Main Program --------
statement = input("Enter a statement: ") # ইউজার ইনপুট নেবে
# statement = "int a = b + 10c + 7;"  
output = lexer(statement)

print("\nLexeme\t\tToken Type")
print("---------------------------")
for lex, typ in output:
    print(f"{lex:10}\t{typ}")
