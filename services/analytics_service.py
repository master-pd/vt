# -*- coding: utf-8 -*-
"""
ANALYTICS SERVICE - DATA ANALYSIS AND REPORTING
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database.database import Database
from database.json_db import JSONDatabase
from utils.logger import Logger

class AnalyticsService:
    def __init__(self):
        self.db = Database()
        self.json_db = JSONDatabase()
        self.logger = Logger("analytics")
    
    def get_daily_analytics(self, date: str = None) -> Dict:
        """Get daily analytics"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get tests for the day
        # This would query database for tests on specific date
        # For now, return sample data
        
        return {
            'date': date,
            'total_tests': 25,
            'total_views_sent': 125000,
            'total_views_verified': 87500,
            'success_rate': 70.0,
            'avg_views_per_test': 5000,
            'avg_duration': 45.5,
            'peak_hour': '14:00-15:00',
            'busiest_hour_tests': 8,
            'most_popular_view_count': 1000,
            'unique_users': 15
        }
    
    def get_weekly_analytics(self, week_start: str = None) -> Dict:
        """Get weekly analytics"""
        if week_start is None:
            # Start of current week (Monday)
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        # This would aggregate daily analytics for the week
        # For now, return sample data
        
        return {
            'week_start': week_start,
            'total_tests': 175,
            'total_views_sent': 875000,
            'total_views_verified': 612500,
            'success_rate': 70.0,
            'avg_daily_tests': 25,
            'avg_daily_views': 125000,
            'growth_rate': 12.5,  # % growth from previous week
            'most_active_day': 'Wednesday',
            'most_active_day_tests': 35,
            'user_retention_rate': 68.2,
            'new_users': 23
        }
    
    def get_monthly_analytics(self, month: str = None) -> Dict:
        """Get monthly analytics"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')
        
        # This would aggregate weekly analytics for the month
        # For now, return sample data
        
        return {
            'month': month,
            'total_tests': 750,
            'total_views_sent': 3750000,
            'total_views_verified': 2625000,
            'success_rate': 70.0,
            'avg_weekly_tests': 187.5,
            'avg_weekly_views': 937500,
            'revenue': 2999.75,  # If paid service
            'cost_per_view': 0.0008,
            'most_active_week': 'Week 2',
            'user_acquisition': 45,
            'user_churn': 12,
            'net_growth': 33
        }
    
    def get_test_analytics(self, test_id: str) -> Dict:
        """Get detailed analytics for a specific test"""
        test = self.db.get_test(test_id)
        
        if not test:
            return {'error': 'Test not found'}
        
        # Calculate additional metrics
        duration = 0
        if test['start_time'] and test['end_time']:
            start = datetime.fromisoformat(test['start_time'])
            end = datetime.fromisoformat(test['end_time'])
            duration = (end - start).total_seconds()
        
        views_per_minute = 0
        if duration > 0:
            views_per_minute = (test['views_sent'] / duration) * 60
        
        efficiency_score = self._calculate_efficiency_score(
            test['success_rate'],
            duration,
            test['views_sent']
        )
        
        return {
            'test_id': test_id,
            'video_url': test['video_url'],
            'target_views': test['target_views'],
            'views_sent': test['views_sent'],
            'views_verified': test['views_verified'],
            'success_rate': test['success_rate'],
            'duration_seconds': duration,
            'views_per_minute': round(views_per_minute, 1),
            'delivery_rate': round((test['views_sent'] / test['target_views']) * 100, 1),
            'verification_rate': round((test['views_verified'] / test['views_sent']) * 100, 1),
            'efficiency_score': efficiency_score,
            'start_time': test['start_time'],
            'end_time': test['end_time'],
            'status': test['status']
        }
    
    def get_user_analytics(self, user_id: int) -> Dict:
        """Get analytics for a specific user"""
        user = self.db.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}
        
        # This would query all tests by this user
        # For now, return sample data
        
        return {
            'user_id': user_id,
            'username': user['username'],
            'join_date': user['join_date'],
            'total_tests': user['total_tests'],
            'total_views_sent': user['total_views'],
            'avg_views_per_test': user['total_views'] / user['total_tests'] if user['total_tests'] > 0 else 0,
            'avg_success_rate': 72.5,  # Would calculate from user's tests
            'favorite_view_count': 1000,
            'most_active_day': 'Friday',
            'test_frequency': '2.3 tests/day',
            'last_test_date': '2024-01-15',
            'success_rate_trend': 'increasing',  # increasing, decreasing, stable
            'efficiency_score': 8.2
        }
    
    def get_system_performance(self) -> Dict:
        """Get system performance metrics"""
        # Get current system status
        current_time = datetime.now()
        
        # Calculate uptime (would need to track start time)
        uptime_seconds = 86400  # 24 hours for example
        
        # Get queue status
        queue = self.json_db.get_queue('pending')
        
        # Get account status
        accounts = self.json_db.get_accounts()
        active_accounts = sum(1 for acc in accounts if acc.get('status') == 'active')
        
        # Get proxy status
        proxies = self.json_db.get_proxies()
        active_proxies = sum(1 for p in proxies if p.get('is_active', False))
        
        # Performance metrics
        performance = {
            'system_uptime': self._format_uptime(uptime_seconds),
            'queue_size': len(queue),
            'active_accounts': active_accounts,
            'active_proxies': active_proxies,
            'total_accounts': len(accounts),
            'total_proxies': len(proxies),
            'account_health': round((active_accounts / len(accounts)) * 100, 1) if accounts else 0,
            'proxy_health': round((active_proxies / len(proxies)) * 100, 1) if proxies else 0,
            'avg_response_time': 125,  # ms
            'error_rate': 0.5,  # %
            'requests_per_minute': 850,
            'system_load': 32.5,  # %
            'memory_usage': '256MB/512MB',
            'disk_usage': '1.2GB/5GB'
        }
        
        return performance
    
    def generate_trend_report(self, days: int = 30) -> Dict:
        """Generate trend report for specified days"""
        trends = {
            'period_days': days,
            'date_range': self._get_date_range(days),
            'metrics': {}
        }
        
        # This would analyze data over the period
        # For now, return sample trends
        
        trends['metrics'] = {
            'total_tests': {'trend': 'up', 'change': 15.2},
            'success_rate': {'trend': 'stable', 'change': 1.5},
            'avg_views_per_test': {'trend': 'up', 'change': 8.7},
            'user_acquisition': {'trend': 'up', 'change': 22.3},
            'system_uptime': {'trend': 'stable', 'change': 0.2},
            'queue_wait_time': {'trend': 'down', 'change': -12.5}
        }
        
        # Identify patterns
        trends['patterns'] = [
            'Peak usage: 14:00-16:00 daily',
            'Highest success rate: Sundays',
            'Most popular view count: 1,000',
            'User retention: 68% after 7 days'
        ]
        
        # Recommendations
        trends['recommendations'] = [
            'Increase proxy pool during peak hours',
            'Optimize account rotation algorithm',
            'Consider adding 2,500 view package',
            'Improve success rate on weekdays'
        ]
        
        return trends
    
    def _calculate_efficiency_score(self, success_rate: float, duration: float, views_sent: int) -> float:
        """Calculate efficiency score (0-10)"""
        if duration <= 0 or views_sent <= 0:
            return 0
        
        # Score based on success rate (max 5 points)
        success_score = (success_rate / 100) * 5
        
        # Score based on speed (max 3 points)
        # Faster is better
        views_per_second = views_sent / duration
        speed_score = min(3, views_per_second / 100)  # 100 views/sec = 3 points
        
        # Score based on reliability (max 2 points)
        # Consistent success rates are better
        reliability_score = 2 if success_rate > 80 else 1 if success_rate > 60 else 0
        
        total_score = success_score + speed_score + reliability_score
        
        return round(min(10, total_score), 1)
    
    def _format_uptime(self, seconds: int) -> str:
        """Format uptime in human readable format"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        
        return ' '.join(parts) if parts else f"{seconds}s"
    
    def _get_date_range(self, days: int) -> str:
        """Get date range string"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        return f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"