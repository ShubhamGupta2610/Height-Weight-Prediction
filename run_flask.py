#!/usr/bin/env python3
"""
Flask app launcher script
Ensures proper path setup and error handling
"""

import os
import sys

def run_flask_app():
    """Run Flask app with proper configuration"""
    app_dir = os.path.join(os.path.dirname(__file__), 'flask_app')
    app_file = os.path.join(app_dir, 'app.py')
    
    if not os.path.exists(app_file):
        print(f"❌ Error: Flask app not found at {app_file}")
        sys.exit(1)
    
    # Add flask_app to path
    sys.path.insert(0, app_dir)
    os.chdir(os.path.dirname(__file__))
    
    try:
        from flask_app.app import app
        print("✅ Flask app loaded successfully")
        print("Opening http://localhost:5000 in your browser...")
        app.run(debug=True, port=5000)
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n✓ Flask app stopped")
        sys.exit(0)

if __name__ == '__main__':
    run_flask_app()
