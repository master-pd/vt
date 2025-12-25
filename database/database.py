# -*- coding: utf-8 -*-
"""
DATABASE HANDLER
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TIMESTAMP,
                total_tests INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT UNIQUE,
                user_id INTEGER,
                video_url TEXT,
                target_views INTEGER,
                views_sent INTEGER DEFAULT 0,
                views_verified INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Accounts table (for TikTok accounts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                status TEXT DEFAULT 'active',
                views_sent INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Proxies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proxy TEXT UNIQUE,
                type TEXT,
                country TEXT,
                speed INTEGER,
                last_used TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # User methods
    def add_user(self, user_id, username, first_name, last_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users 
            (user_id, username, first_name, last_name, join_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = ['id', 'user_id', 'username', 'first_name', 'last_name', 
                      'join_date', 'total_tests', 'total_views', 'is_active']
            return dict(zip(columns, row))
        return None
    
    # Test methods
    def create_test(self, test_id, user_id, video_url, target_views):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tests 
            (test_id, user_id, video_url, target_views, start_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (test_id, user_id, video_url, target_views, datetime.now()))
        
        conn.commit()
        conn.close()
        return True
    
    def update_test(self, test_id, views_sent, views_verified, status='completed'):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        success_rate = 0
        if views_sent > 0:
            success_rate = (views_verified / views_sent) * 100
        
        cursor.execute('''
            UPDATE tests 
            SET views_sent = ?, views_verified = ?, success_rate = ?, 
                end_time = ?, status = ?
            WHERE test_id = ?
        ''', (views_sent, views_verified, success_rate, datetime.now(), status, test_id))
        
        # Update user stats
        test = self.get_test(test_id)
        if test:
            cursor.execute('''
                UPDATE users 
                SET total_tests = total_tests + 1,
                    total_views = total_views + ?
                WHERE user_id = ?
            ''', (views_sent, test['user_id']))
        
        conn.commit()
        conn.close()
    
    def get_test(self, test_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tests WHERE test_id = ?', (test_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = ['id', 'test_id', 'user_id', 'video_url', 'target_views',
                      'views_sent', 'views_verified', 'success_rate', 
                      'start_time', 'end_time', 'status']
            return dict(zip(columns, row))
        return None
    
    # Statistics methods
    def get_statistics(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total tests
        cursor.execute('SELECT COUNT(*) FROM tests')
        total_tests = cursor.fetchone()[0]
        
        # Total views sent
        cursor.execute('SELECT SUM(views_sent) FROM tests')
        total_views = cursor.fetchone()[0] or 0
        
        # Today's tests
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM tests WHERE DATE(start_time) = ?', (today,))
        today_tests = cursor.fetchone()[0]
        
        # Today's views
        cursor.execute('SELECT SUM(views_sent) FROM tests WHERE DATE(start_time) = ?', (today,))
        today_views = cursor.fetchone()[0] or 0
        
        # Active accounts
        cursor.execute('SELECT COUNT(*) FROM accounts WHERE status = "active"')
        active_accounts = cursor.fetchone()[0]
        
        # Average success rate
        cursor.execute('SELECT AVG(success_rate) FROM tests WHERE success_rate > 0')
        avg_success = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_tests': total_tests,
            'total_views': total_views,
            'today_tests': today_tests,
            'today_views': today_views,
            'active_accounts': active_accounts,
            'success_rate': round(avg_success, 2)
        }