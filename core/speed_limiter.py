# -*- coding: utf-8 -*-
"""
SPEED LIMITER - CONTROL VIEW SENDING SPEED
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import time
from datetime import datetime
from typing import Dict
from utils.logger import Logger

class SpeedLimiter:
    def __init__(self, max_views_per_minute: int = 10000):
        self.max_views_per_minute = max_views_per_minute
        self.views_sent = 0
        self.minute_start = time.time()
        self.logger = Logger("speed_limiter")
        
        # Calculate delay between requests
        self.request_delay = 60.0 / max_views_per_minute if max_views_per_minute > 0 else 0
        
        self.logger.info(f"Speed limiter initialized: {max_views_per_minute} views/min, delay: {self.request_delay:.3f}s")
    
    def can_send(self) -> bool:
        """Check if we can send another view"""
        current_time = time.time()
        elapsed = current_time - self.minute_start
        
        # Reset counter every minute
        if elapsed >= 60:
            self.views_sent = 0
            self.minute_start = current_time
            self.logger.debug("Speed limiter minute reset")
        
        # Check if we've reached the limit
        if self.views_sent >= self.max_views_per_minute:
            wait_time = 60 - elapsed
            if wait_time > 0:
                self.logger.warning(f"Rate limit reached, waiting {wait_time:.1f} seconds")
                time.sleep(wait_time)
                self.views_sent = 0
                self.minute_start = time.time()
        
        return True
    
    def record_send(self):
        """Record that a view was sent"""
        self.views_sent += 1
        
        # Log progress every 100 views
        if self.views_sent % 100 == 0:
            elapsed = time.time() - self.minute_start
            current_speed = (self.views_sent / elapsed) * 60 if elapsed > 0 else 0
            self.logger.debug(f"Views sent: {self.views_sent}, Current speed: {current_speed:.0f}/min")
    
    def get_wait_time(self) -> float:
        """Calculate how long to wait before next request"""
        if self.request_delay <= 0:
            return 0
        
        # Add some randomness to avoid pattern detection
        random_factor = 1.0 + (random.random() * 0.2 - 0.1)  # ±10%
        return self.request_delay * random_factor
    
    def get_current_speed(self) -> float:
        """Get current sending speed"""
        elapsed = time.time() - self.minute_start
        if elapsed <= 0:
            return 0
        
        current_speed = (self.views_sent / elapsed) * 60
        return current_speed
    
    def get_status(self) -> Dict:
        """Get speed limiter status"""
        elapsed = time.time() - self.minute_start
        current_speed = self.get_current_speed()
        remaining = max(0, 60 - elapsed)
        
        return {
            'max_views_per_minute': self.max_views_per_minute,
            'views_sent_this_minute': self.views_sent,
            'current_speed': round(current_speed, 1),
            'time_elapsed': round(elapsed, 1),
            'time_remaining': round(remaining, 1),
            'request_delay': round(self.request_delay, 3),
            'limit_usage_percent': (self.views_sent / self.max_views_per_minute) * 100
        }
    
    def adjust_speed(self, new_speed: int):
        """Adjust maximum speed"""
        old_speed = self.max_views_per_minute
        self.max_views_per_minute = new_speed
        self.request_delay = 60.0 / new_speed if new_speed > 0 else 0
        
        self.logger.info(f"Speed adjusted: {old_speed} -> {new_speed} views/min")
    
    def reset(self):
        """Reset the speed limiter"""
        self.views_sent = 0
        self.minute_start = time.time()
        self.logger.debug("Speed limiter reset")