# -*- coding: utf-8 -*-
"""
USER MANAGEMENT SYSTEM
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database.database import Database
from utils.logger import bot_logger

class UserManager:
    def __init__(self):
        self.db = Database()
        self.user_sessions = {}  # user_id -> session_data
        self.user_activity = {}  # user_id -> last_activity
        self.user_limits = {}    # user_id -> usage_limits
        
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user information"""
        return self.db.get_user(user_id)
    
    def create_user(self, user_id: int, username: str, first_name: str, last_name: str = "") -> bool:
        """Create new user"""
        user = self.get_user(user_id)
        
        if user:
            # Update existing user
            self.update_user_activity(user_id)
            return False
        
        # Add new user
        self.db.add_user(user_id, username, first_name, last_name)
        
        # Initialize user limits
        self.user_limits[user_id] = {
            'daily_tests': 0,
            'daily_views': 0,
            'max_tests_per_day': 10,
            'max_views_per_day': 100000,
            'last_reset': datetime.now().date().isoformat()
        }
        
        bot_logger.info(f"New user created: {user_id} - @{username}")
        return True
    
    def update_user_activity(self, user_id: int):
        """Update user last activity"""
        self.user_activity[user_id] = time.time()
        
        # Update in database if needed
        # This could be done periodically instead of every time
    
    def get_user_session(self, user_id: int) -> Dict:
        """Get or create user session"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'user_id': user_id,
                'created_at': time.time(),
                'data': {},
                'test_queue': [],
                'current_test': None
            }
        
        return self.user_sessions[user_id]
    
    def update_user_session(self, user_id: int, key: str, value):
        """Update user session data"""
        session = self.get_user_session(user_id)
        session['data'][key] = value
        session['last_updated'] = time.time()
    
    def get_user_session_data(self, user_id: int, key: str, default=None):
        """Get data from user session"""
        session = self.get_user_session(user_id)
        return session['data'].get(key, default)
    
    def can_user_start_test(self, user_id: int, view_count: int) -> tuple:
        """Check if user can start a new test"""
        user = self.get_user(user_id)
        
        if not user:
            return False, "User not found"
        
        # Check if user is active
        if not user.get('is_active', True):
            return False, "Account is inactive"
        
        # Check daily limits
        limits = self.user_limits.get(user_id, {})
        today = datetime.now().date().isoformat()
        
        # Reset daily counters if new day
        if limits.get('last_reset') != today:
            limits['daily_tests'] = 0
            limits['daily_views'] = 0
            limits['last_reset'] = today
        
        # Check test limit
        if limits['daily_tests'] >= limits['max_tests_per_day']:
            return False, f"Daily test limit reached ({limits['max_tests_per_day']})"
        
        # Check view limit
        if limits['daily_views'] + view_count > limits['max_views_per_day']:
            return False, f"Daily view limit exceeded"
        
        # Check if user has ongoing test
        session = self.get_user_session(user_id)
        if session['current_test']:
            return False, "You have an ongoing test"
        
        return True, "OK"
    
    def start_user_test(self, user_id: int, test_id: str, view_count: int):
        """Record that user started a test"""
        session = self.get_user_session(user_id)
        session['current_test'] = test_id
        
        # Update limits
        limits = self.user_limits.get(user_id, {})
        limits['daily_tests'] = limits.get('daily_tests', 0) + 1
        limits['daily_views'] = limits.get('daily_views', 0) + view_count
        
        # Update database
        # Increment user's total tests count
        # This would be done when test completes
    
    def complete_user_test(self, user_id: int, test_id: str):
        """Record that user completed a test"""
        session = self.get_user_session(user_id)
        if session['current_test'] == test_id:
            session['current_test'] = None
        
        # Add to test history
        if 'test_history' not in session['data']:
            session['data']['test_history'] = []
        
        session['data']['test_history'].append({
            'test_id': test_id,
            'completed_at': time.time()
        })
        
        # Keep only last 50 tests
        if len(session['data']['test_history']) > 50:
            session['data']['test_history'] = session['data']['test_history'][-50:]
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get user statistics"""
        user = self.get_user(user_id)
        
        if not user:
            return {}
        
        session = self.get_user_session(user_id)
        limits = self.user_limits.get(user_id, {})
        
        return {
            'user_id': user_id,
            'username': user.get('username'),
            'join_date': user.get('join_date'),
            'total_tests': user.get('total_tests', 0),
            'total_views': user.get('total_views', 0),
            'daily_tests': limits.get('daily_tests', 0),
            'daily_views': limits.get('daily_views', 0),
            'daily_limits': {
                'max_tests': limits.get('max_tests_per_day', 10),
                'max_views': limits.get('max_views_per_day', 100000)
            },
            'current_test': session.get('current_test'),
            'test_history_count': len(session['data'].get('test_history', [])),
            'last_activity': self.user_activity.get(user_id)
        }
    
    def get_all_users(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all users (for admin)"""
        # This would query database for all users
        # For now, return sample data
        return []
    
    def update_user_limits(self, user_id: int, limits: Dict):
        """Update user limits (admin function)"""
        if user_id in self.user_limits:
            self.user_limits[user_id].update(limits)
            return True
        return False
    
    def get_active_users_count(self, hours: int = 24) -> int:
        """Count users active in last X hours"""
        cutoff = time.time() - (hours * 3600)
        active = 0
        
        for user_id, last_active in self.user_activity.items():
            if last_active > cutoff:
                active += 1
        
        return active
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Cleanup old user sessions"""
        cutoff = time.time() - (max_age_hours * 3600)
        removed = 0
        
        for user_id in list(self.user_sessions.keys()):
            session = self.user_sessions[user_id]
            if session['created_at'] < cutoff:
                # Check if user has been inactive
                last_activity = self.user_activity.get(user_id, 0)
                if last_activity < cutoff:
                    del self.user_sessions[user_id]
                    removed += 1
        
        if removed > 0:
            bot_logger.info(f"Cleaned up {removed} old user sessions")
        
        return removed