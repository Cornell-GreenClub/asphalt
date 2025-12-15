"""
Central configuration file for the TSP route optimizer.
Holds all constants and server settings.
"""

import os

# === SERVER SETTINGS ===
FLASK_HOST = '0.0.0.0'
FLASK_PORT = int(os.environ.get('PORT', 8000))
OSRM_HOST = os.environ.get('OSRM_HOST', "http://127.0.0.1:5000")