# -*- coding: utf-8 -*-
"""
LOGGER - ADVANCED LOGGING SYSTEM
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from config import Config

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        logs_dir = Config.LOGS_DIR
        logs_dir.mkdir(exist_ok=True)
        
        # Log file with date
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def critical(self, message: str):
        self.logger.critical(message)
    
    def log_with_data(self, level: str, message: str, data: dict = None):
        """Log message with additional data"""
        if data:
            message = f"{message} | Data: {data}"
        
        if level == 'info':
            self.info(message)
        elif level == 'warning':
            self.warning(message)
        elif level == 'error':
            self.error(message)
        elif level == 'debug':
            self.debug(message)
        elif level == 'critical':
            self.critical(message)

def setup_logger(name: str) -> Logger:
    """Setup and return a logger instance"""
    return Logger(name)

# Global logger instances
system_logger = setup_logger("system")
database_logger = setup_logger("database")
bot_logger = setup_logger("telegram_bot")
view_logger = setup_logger("view_engine")