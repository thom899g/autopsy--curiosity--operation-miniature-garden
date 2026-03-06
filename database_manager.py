"""
Firebase database manager for Operation Miniature Garden.
Handles all database operations with retry logic and error handling.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
from dataclasses import asdict

import firebase_admin
from firebase_admin import credentials,