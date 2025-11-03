"""Vercel serverless function - imports Flask app"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app
from app import app

# Vercel expects 'app' to be exported
__all__ = ['app']
