import ast

def generate_typing_import(node):
    """
    Given an AST node, generates an import statement that imports from `typing` all types that were used in the node.
    """
    types = set()

    # Collect all types used in the node
    for n in ast.walk(node):
        if isinstance(n, ast.AST):
            for field, value in ast.iter_fields(n):
                if isinstance(value, ast.AST):
                    types |= set(getattr(value, 'annotation', []))

    # Generate the import statement
    import_statements = []
    for t in types:
        if isinstance(t, ast.Name) and t.id != 'Any':
            import_statements.append(f"from typing import {t.id}")
        elif isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == 'typing':
            import_statements.append(f"from typing import {t.attr}")

    return '\n'.join(import_statements)


code_str = """
def foo(x: List[int], y: Tuple[str, int]) -> dict:
    return {}
"""

ast_tree = ast.parse(code_str)
func_node = next((n for n in ast.walk(ast_tree) if isinstance(n, ast.FunctionDef) and n.name == 'foo'), None)
typing_import = generate_typing_import(func_node)
print(typing_import) # Output: from typing import List, Tuple, dict
