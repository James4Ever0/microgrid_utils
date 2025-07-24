#!/bin/bash

OUTPUT_DIR="./requirements_txt"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Find all Python files and process them
ls -1 | grep -E '.*.py$' | sed 's|^\./||' | while read -r pyfile; do
    # Generate dependencies for each Python file
cat <<EOF  > /tmp/find_import.py
import ast
import os
import sys

def get_imports(file_path, local_modules):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imp = alias.name.split('.')[0]
                if imp not in local_modules:
                    imports.add(imp)
        elif isinstance(node, ast.ImportFrom):
            # Skip relative imports (local to package)
            if node.level > 0:
                continue
            if node.module:
                imp = node.module.split('.')[0]
                if imp not in local_modules:
                    imports.add(imp)
    return imports

def main():
    python_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(python_file):
        print(f"File not found: {python_file}")
        return
    
    # Get the directory of the current Python file
    file_dir = os.path.dirname(python_file) or '.'  # handle current directory
    
    # Identify local modules in the same directory
    local_modules = set()
    if os.path.exists(file_dir):
        for fname in os.listdir(file_dir):
            if fname.endswith('.py'):
                module_name = os.path.splitext(fname)[0]
                local_modules.add(module_name)
    
    imports = get_imports(python_file, local_modules)
    
    # Get base filename without .py extension
    base_name = os.path.splitext(os.path.basename(python_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}_requirements.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for imp in sorted(imports):
            f.write(f"{imp}\\n")
    print(f"Generated: {output_file}")

if __name__ == "__main__":
    main()
EOF
python3 /tmp/find_import.py    "$pyfile" "$OUTPUT_DIR"
done
