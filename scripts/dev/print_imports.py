import ast
from pathlib import Path
from typing import Set, Dict, List
import re

def get_package_name(import_name: str) -> str:
    """Convert import name to package name (e.g., 'pandas.core' -> 'pandas')"""
    return import_name.split('.')[0]

def get_imports(file_path: Path) -> Set[str]:
    with open(file_path, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except:
            print(f"Failed to parse: {file_path}")
            return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.add(get_package_name(name.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(get_package_name(node.module))
    return imports

def read_requirements(filename: str) -> Dict[str, str]:
    packages = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name and version
                match = re.match(r'([^>=<]+)([>=<]+[^,\s]+)?', line)
                if match:
                    pkg, version = match.groups()
                    packages[pkg.lower()] = version or ''
    return packages

def scan_project(project_root: str = "src/tarotai") -> Set[str]:
    all_imports = set()
    root = Path(project_root)
    for py_file in root.rglob("*.py"):
        if "__pycache__" not in str(py_file):
            imports = get_imports(py_file)
            all_imports.update(imports)
    return all_imports

if __name__ == "__main__":
    # Get all imports from the project
    used_imports = scan_project()
    
    # Read requirements
    req_packages = read_requirements('requirements.txt')
    pyproject_packages = read_requirements('pyproject.toml')  # This might need adjustment
    
    print("\nPackages used in code:")
    for imp in sorted(used_imports):
        print(f"  {imp}")
    
    print("\nUnused packages in requirements.txt:")
    for pkg in sorted(req_packages):
        if pkg not in [imp.lower() for imp in used_imports]:
            print(f"  {pkg}{req_packages[pkg]}")
    
    print("\nMissing packages (used but not in requirements):")
    for imp in sorted(used_imports):
        if imp.lower() not in req_packages:
            print(f"  {imp}")