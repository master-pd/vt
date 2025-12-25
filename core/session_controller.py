# -*- coding: utf-8 -*-
"""
SESSION CONTROLLER - MANAGE USER SESSIONS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from database.database import Database
from utils.logger import Logger

class SessionController:
    def __init__(self):
        self.db = Database()
        self.logger = Logger("session_controller")
        self.sessions = {}  # In-memory session storage
        self.session_timeout = 3600  # 1 hour
        
    def create_session(self, user_id: int, user_data: Dict) -> str:
        """Create a new session for user"""
        # Generate session ID
        session_data = f"{user_id}{time.time()}{random.random()}"
        session_id = hashlib.sha256(session_data.encode()).hexdigest()[:32]
        
        # Store session
        self.sessions[session_id] = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'ip_address': user_data.get('ip', ''),
            'user_agent': user_data.get('user_agent', '')
        }
        
        self.logger.info(f"Session created for user {user_id}: {session_id[:8]}...")
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """Validate and return session data"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session expired
        last_activity = session['last_activity']
        if datetime.now() - last_activity > timedelta(seconds=self.session_timeout):
            self.logger.info(f"Session expired: {session_id[:8]}...")
            del self.sessions[session_id]
            return None
        
        # Update last activity
        session['last_activity'] = datetime.now()
        
        return session
    
    def destroy_session(self, session_id: str) -> bool:
        """Destroy a session"""
        if session_id in self.sessions:
            user_id = self.sessions[session_id]['user_id']
            del self.sessions[session_id]
            self.logger.info(f"Session destroyed for user {user_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        expired = []
        now = datetime.now()
        
        for session_id, session in self.sessions.items():
            last_activity = session['last_activity']
            if now - last_activity > timedelta(seconds=self.session_timeout):
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            self.logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_user_sessions(self, user_id: int) -> List[str]:
        """Get all active sessions for a user"""
        user_sessions = []
        
        for session_id, session in self.sessions.items():
            if session['user_id'] == user_id:
                user_sessions.append(session_id)
        
        return user_sessions
    
    def get_session_count(self) -> Dict:
        """Get session statistics"""
        total = len(self.sessions)
        
        # Count by age
        now = datetime.now()
        recent = 0
        old = 0
        
        for session in self.sessions.values():
            age = now - session['last_activity']
            if age < timedelta(minutes=30):
                recent += 1
            else:
                old += 1
        
        return {
            'total_sessions': total,
            'recent_sessions': recent,
            'old_sessions': old,
            'session_timeout': self.session_timeout
        }