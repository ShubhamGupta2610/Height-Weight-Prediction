"""
Project structure initialization
"""

import os

# Define project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define key directories
DIRS = {
    'data': os.path.join(PROJECT_ROOT, 'data'),
    'notebooks': os.path.join(PROJECT_ROOT, 'notebooks'),
    'streamlit': os.path.join(PROJECT_ROOT, 'streamlit_app'),
    'flask': os.path.join(PROJECT_ROOT, 'flask_app'),
    'docs': os.path.join(PROJECT_ROOT, 'docs'),
    'config': os.path.join(PROJECT_ROOT, 'config'),
    'scripts': os.path.join(PROJECT_ROOT, 'scripts'),
}

# Create directories if they don't exist
for dir_path in DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

__all__ = ['PROJECT_ROOT', 'DIRS']
