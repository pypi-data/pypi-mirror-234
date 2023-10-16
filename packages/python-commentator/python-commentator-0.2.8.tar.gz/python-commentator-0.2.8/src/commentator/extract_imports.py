def extract_imports(code_str):
    # Parse the input code string into an Abstract Syntax Tree (AST)
    tree = ast.parse(code_str)
    
    # Initialize an empty list to store the import statements
    imports = []
    
    # Traverse the AST and find all import statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # Add the entire import statement as a string to the list
            imports.append(ast.unparse(node).strip())
        elif isinstance(node, ast.ImportFrom):
            # Add the entire import statement as a string to the list
            imports.append(ast.unparse(node).strip())
    
    # Join the list of import statements into a single string, separated by newlines
    return '\n'.join(imports)

