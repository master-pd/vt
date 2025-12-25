# -*- coding: utf-8 -*-
"""
CONFIGURATION FILE
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
import os
from pathlib import Path

class Config:
    # ========== PROJECT INFO ==========
    PROJECT_NAME = "VT VIEW TESTER"
    VERSION = "2.0.0"
    AUTHOR = "MASTER (RANA)"
    TEAM = "MAR PD"
    
    # ========== PATHS ==========
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = DATA_DIR / "logs"
    
    # ========== DATABASE ==========
    DATABASE_PATH = DATA_DIR / "users.db"
    ACCOUNTS_FILE = DATA_DIR / "accounts.json"
    PROXIES_FILE = DATA_DIR / "proxies.json"
    
    # ========== TIKTOK SETTINGS ==========
    MAX_VIEWS_PER_MINUTE = 10000
    MIN_VIEWS = 10
    MAX_VIEWS = 10000
    DEFAULT_VIEWS = 1000
    
    # ========== TELEGRAM BOT ==========
    BOT_TOKEN = "7488701410:AAEyOD9mMw060j30sNkV-2ZEapMIIfaXa0A"  # Add your bot token here
    ADMIN_IDS = [6454347745]  # Add admin user IDs
    
    # ========== REQUEST SETTINGS ==========
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    DELAY_BETWEEN_REQUESTS = 0.5
    
    # ========== SECURITY ==========
    MAX_SESSIONS_PER_IP = 5
    RATE_LIMIT_WINDOW = 60
    
    # ========== STYLING ==========
    TERMINAL_WIDTH = 80
    BORDER_CHAR = "═"
    LINE_CHAR = "─"
    
    @classmethod
    def load_json(cls, file_path):
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    @classmethod
    def save_json(cls, file_path, data):
        """Save JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)