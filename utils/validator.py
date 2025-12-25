# -*- coding: utf-8 -*-
"""
VALIDATOR - INPUT VALIDATION AND SANITIZATION
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import re
from urllib.parse import urlparse
from typing import Tuple, Optional

class Validator:
    @staticmethod
    def validate_tiktok_url(url: str) -> Tuple[bool, str]:
        """Validate TikTok URL"""
        if not url:
            return False, "URL cannot be empty"
        
        # Clean URL
        url = url.strip()
        
        # Check common TikTok URL patterns
        patterns = [
            r'https?://(www\.|vm\.|vt\.)?tiktok\.com/',
            r'https?://tiktok\.com/@[\w\.-]+/video/\d+',
            r'https?://vm\.tiktok\.com/[\w]+/',
            r'https?://vt\.tiktok\.com/[\w]+/'
        ]
        
        for pattern in patterns:
            if re.match(pattern, url):
                return True, "Valid TikTok URL"
        
        return False, "Invalid TikTok URL format"
    
    @staticmethod
    def validate_view_count(count: int, min_views: int = 10, max_views: int = 10000) -> Tuple[bool, str]:
        """Validate view count"""
        if not isinstance(count, int):
            return False, "View count must be a number"
        
        if count < min_views:
            return False, f"Minimum views is {min_views}"
        
        if count > max_views:
            return False, f"Maximum views is {max_views}"
        
        return True, "Valid view count"
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from TikTok URL"""
        # Pattern 1: /video/1234567890
        pattern1 = r'/video/(\d+)'
        match1 = re.search(pattern1, url)
        if match1:
            return match1.group(1)
        
        # Pattern 2: Short URL - extract and follow redirect
        # For short URLs, we'd need to resolve them
        if 'vm.tiktok.com' in url or 'vt.tiktok.com' in url:
            # Return the short code
            parts = url.strip('/').split('/')
            if parts:
                return parts[-1]
        
        return None
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate TikTok username"""
        if not username:
            return False, "Username cannot be empty"
        
        username = username.strip()
        
        # TikTok username pattern
        pattern = r'^[a-zA-Z0-9._]+$'
        
        if not re.match(pattern, username):
            return False, "Invalid username format"
        
        if len(username) < 2:
            return False, "Username too short"
        
        if len(username) > 24:
            return False, "Username too long"
        
        return True, "Valid username"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password"""
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        return True, "Valid password"
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 500) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Escape special characters for SQL
        text = text.replace("'", "''").replace('"', '""')
        
        return text
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email address"""
        if not email:
            return False, "Email cannot be empty"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, "Valid email"
    
    @staticmethod
    def validate_proxy(proxy: str) -> Tuple[bool, str]:
        """Validate proxy format"""
        if not proxy:
            return False, "Proxy cannot be empty"
        
        # Common proxy patterns
        patterns = [
            r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$',  # ip:port
            r'^[^:]+:[^@]+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$',  # user:pass@ip:port
            r'^https?://',  # http://...
            r'^socks[45]://'  # socks4:// or socks5://
        ]
        
        for pattern in patterns:
            if re.match(pattern, proxy):
                return True, "Valid proxy format"
        
        return False, "Invalid proxy format"
    
    @staticmethod
    def validate_test_id(test_id: str) -> Tuple[bool, str]:
        """Validate test ID format"""
        if not test_id:
            return False, "Test ID cannot be empty"
        
        pattern = r'^VT-\d+$|^[A-Z0-9]{8}$'
        
        if re.match(pattern, test_id):
            return True, "Valid test ID"
        
        return False, "Invalid test ID format"