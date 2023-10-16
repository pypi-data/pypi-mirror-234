import ast_comments as ast

def get_typing_imports(ast_tree):
    """
    Given an AST object, returns a list of import statements for all imports from the `typing` library
    """
    typing_imports = []
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] == 'typing':
                    typing_imports.append(ast.unparse(node).strip())
                    break
        elif isinstance(node, ast.ImportFrom):
            if node.module.split('.')[0] == 'typing':
                for alias in node.names:
                    typing_imports.append(ast.unparse(node).strip())
                    break
    return typing_imports

x = """import foo
import bar as potato
import typing
from typing import Moop

def banana():
  import typing as Soda
"""

print(get_typing_imports(ast.parse(x)))

