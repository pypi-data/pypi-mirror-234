import ast_comments as ast

class TypeCollector(ast.NodeVisitor):

    def __init__(self):
        self.types = set()

    def types(self):
        return self.types
    
    def visit_Assign(self, node):
        if node.type_comment:
            self.types.add(node.type_comment)
    
    def visit_Name(self, node):
        if node.annotation:
            self.types.add(node.annotation)

    def visit_For(self, node):
        if node.type_comment:
            self.types.add(node.type_comment)

    def visit_With(self, node):
        if node.type_comment:
            self.types.add(node.type_comment)

    def visit_AsyncFunctionDef(self, node):
        self.process_function(node)
    
    def visit_FunctionDef(self, node):
        self.process_function(node)

    def visit_arguments(self, node):
        for arg in node.args:
            if arg.annotation:
                self.types.add(arg.annotation)
        if node.vararg:
            if node.vararg.annotation:
                self.types.add(node.vararg.annotation)
        if node.kwarg:
            if node.kwarg.annotation:
                self.types.add(node.kwarg.annotation)
        return node
    
    def process_function(self, node):
        if node.returns:
            self.types.add(node.returns)
        if node.type_comment:
            self.types.add(node.type_comment)
        self.generic_visit(node)
    
    def visit_arg(self, node):
        if node.type_comment:
            self.types.add(node.type_comment)
    
    def visit_AnnAssign(self, node):
        if node.annotation:
            self.types.add(node.annotation)

def collect_types(node):
    return (TypeCollector().visit(node)).types()
