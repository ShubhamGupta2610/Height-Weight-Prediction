"""
Project structure visualization script
"""

import os
from pathlib import Path

def print_tree(directory, prefix="", max_depth=3, current_depth=0, ignore_dirs=None):
    """Print directory tree structure"""
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.egg-info'}
    
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        return
    
    # Filter ignored directories
    items = [item for item in items if item not in ignore_dirs]
    
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
    
    # Print files
    for i, file in enumerate(files):
        is_last = (i == len(files) - 1) and len(dirs) == 0
        print(f"{prefix}{'└── ' if is_last else '├── '}{file}")
    
    # Print directories
    for i, dir_name in enumerate(dirs):
        is_last = i == len(dirs) - 1
        print(f"{prefix}{'└── ' if is_last else '├── '}{dir_name}/")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_tree(os.path.join(directory, dir_name), new_prefix, max_depth, current_depth + 1, ignore_dirs)

def main():
    """Print project structure"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n📁 Height-Weight Predictor Project Structure")
    print("=" * 50)
    print(f"\nRoot: {project_root}\n")
    print_tree(project_root)
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()
