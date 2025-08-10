import os
import re
import subprocess
import sys

def find_imports_from_file(filepath):
    """Extract top-level imports from a Python file."""
    imports = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            # Match 'import x' or 'from x import y'
            match = re.match(r'^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)', line)
            if match:
                module = match.group(1).split(".")[0]
                imports.add(module)
    return imports

def get_all_imports(root_dir="."):
    """Scan all .py files recursively for imports."""
    all_imports = set()
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(subdir, file)
                all_imports.update(find_imports_from_file(filepath))
    return all_imports

def is_standard_library(module):
    """Check if module is part of the Python standard library."""
    try:
        # If we can import it without pip installing, and it's in sys.stdlib_module_names (Python 3.10+)
        if hasattr(sys, "stdlib_module_names"):
            return module in sys.stdlib_module_names
        else:
            import importlib.util
            spec = importlib.util.find_spec(module)
            if spec and spec.origin and "site-packages" not in spec.origin:
                return True
    except ModuleNotFoundError:
        return False
    return False

def map_to_pypi_packages(modules):
    """Filter out standard library modules and return pip package names."""
    packages = []
    for module in modules:
        if not is_standard_library(module):
            packages.append(module)
    return sorted(set(packages))

if __name__ == "__main__":
    print("🔍 Scanning for imports...")
    all_imports = get_all_imports(".")
    packages = map_to_pypi_packages(all_imports)

    # Save to requirements.txt
    with open("requirements.txt", "w", encoding="utf-8") as f:
        for pkg in packages:
            f.write(pkg + "\n")

    print(f"✅ requirements.txt generated with {len(packages)} packages:")
    for pkg in packages:
        print(f" - {pkg}")
