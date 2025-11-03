# Vercel serverless function for Flask app
# This is the entry point for all requests

import sys
import os
import time

# Track import time for diagnostics
_import_start = time.time()

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_path_time = time.time() - _import_start
print(f"[API] Path setup took {_path_time:.3f}s")

# Import the Flask app (this will trigger app.py initialization)
_import_app_start = time.time()
from app import app
_import_app_time = time.time() - _import_app_start
print(f"[API] Flask app import took {_import_app_time:.2f}s")

_total_import = time.time() - _import_start
print(f"[API] Total api/index.py initialization: {_total_import:.2f}s")

# Export the app - Vercel's @vercel/python runtime will handle it automatically
__all__ = ['app']
