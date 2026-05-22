import ast
from pathlib import Path

def test():
    source = Path("ai_toolkit.py").read_text()
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            print(f"Top-level import: {ast.dump(node)}")

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "groq":
             # Find if it's top level
             is_top = any(node == child for child in ast.iter_child_nodes(tree))
             print(f"Found groq import, top level: {is_top}")

if __name__ == '__main__':
    test()
