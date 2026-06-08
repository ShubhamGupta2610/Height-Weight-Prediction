#!/usr/bin/env python3
"""
Streamlit app launcher script
Ensures proper path setup and error handling
"""

import os
import sys
import subprocess

def run_streamlit_app():
    """Run Streamlit app with proper configuration"""
    app_path = os.path.join(os.path.dirname(__file__), 'streamlit_app', 'app.py')
    
    if not os.path.exists(app_path):
        print(f"❌ Error: App file not found at {app_path}")
        sys.exit(1)
    
    try:
        subprocess.run([
            'streamlit', 'run', app_path,
            '--server.port', '8501',
            '--server.address', 'localhost'
        ], check=True)
    except FileNotFoundError:
        print("❌ Error: Streamlit not installed")
        print("Install with: pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✓ Streamlit app stopped")
        sys.exit(0)

if __name__ == '__main__':
    run_streamlit_app()
