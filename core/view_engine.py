# -*- coding: utf-8 -*-
"""
VIEW ENGINE - MAIN VIEW SENDING SYSTEM
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import asyncio
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from database.database import Database
from database.json_db import JSONDatabase
from utils.logger import Logger
from config import Config

class ViewEngine:
    def __init__(self):
        self.db = Database()
        self.json_db = JSONDatabase()
        self.logger = Logger("view_engine")
        self.active_tests = {}
        self.is_running = False
        
    async def send_views(self, video_url: str, target_views: int, test_id: str, user_id: int = None) -> Dict:
        """Main view sending function"""
        self.active_tests[test_id] = {
            'start_time': datetime.now(),
            'sent': 0,
            'verified': 0,
            'status': 'running'
        }
        
        self.is_running = True
        views_sent = 0
        batch_size = min(100, target_views)
        
        self.logger.info(f"Starting test {test_id}: {target_views} views to {video_url}")
        
        # Get available accounts and proxies
        accounts = self.json_db.get_accounts()
        proxies = self.json_db.get_proxies()
        
        if not accounts:
            self.logger.error("No accounts available")
            return {'error': 'No accounts available'}
        
        # Start sending views in batches
        while views_sent < target_views and self.is_running:
            batch_target = min(batch_size, target_views - views_sent)
            batch_sent = await self._send_batch(video_url, batch_target, accounts, proxies)
            
            views_sent += batch_sent
            self.active_tests[test_id]['sent'] = views_sent
            
            # Update progress
            progress = (views_sent / target_views) * 100
            speed = batch_sent * (60 / Config.DELAY_BETWEEN_REQUESTS)
            
            self.logger.info(f"Test {test_id}: {views_sent}/{target_views} ({progress:.1f}%) - Speed: {speed:.0f}/min")
            
            # Small delay between batches
            if views_sent < target_views:
                await asyncio.sleep(1)
        
        # Get final verified views (simulated)
        verified_views = self._simulate_verification(views_sent)
        self.active_tests[test_id]['verified'] = verified_views
        self.active_tests[test_id]['status'] = 'completed'
        
        # Calculate success rate
        success_rate = 0
        if views_sent > 0:
            success_rate = (verified_views / views_sent) * 100
        
        # Update database
        if user_id:
            self.db.update_test(test_id, views_sent, verified_views)
        
        result = {
            'test_id': test_id,
            'views_sent': views_sent,
            'views_verified': verified_views,
            'success_rate': round(success_rate, 2),
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"Test {test_id} completed: {views_sent} sent, {verified_views} verified ({success_rate:.1f}%)")
        return result
    
    async def _send_batch(self, video_url: str, batch_size: int, accounts: List, proxies: List) -> int:
        """Send a batch of views"""
        tasks = []
        sent_count = 0
        
        for i in range(batch_size):
            if not self.is_running:
                break
            
            # Rotate account
            account = accounts[i % len(accounts)]
            
            # Rotate proxy if available
            proxy = None
            if proxies:
                proxy = proxies[i % len(proxies)]
            
            # Create view task
            task = self._send_single_view(video_url, account, proxy)
            tasks.append(task)
            
            # Control speed
            delay = Config.DELAY_BETWEEN_REQUESTS + random.uniform(-0.1, 0.1)
            await asyncio.sleep(delay)
        
        # Execute all tasks
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            sent_count = sum(1 for r in results if r is True)
        
        return sent_count
    
    async def _send_single_view(self, video_url: str, account: Dict, proxy: Dict = None) -> bool:
        """Send a single view"""
        try:
            # Simulate view sending
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Update account usage
            self.json_db.update_account_usage(account['username'])
            
            # Random success/failure
            success = random.random() > 0.1  # 90% success rate
            
            if success:
                self.logger.debug(f"View sent from {account['username']} to {video_url}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send view: {e}")
            return False
    
    def _simulate_verification(self, sent_views: int) -> int:
        """Simulate TikTok view verification"""
        # Real verification would check actual view count
        # Here we simulate with 60-80% success rate
        min_rate = 0.6
        max_rate = 0.8
        
        success_rate = random.uniform(min_rate, max_rate)
        verified = int(sent_views * success_rate)
        
        return verified
    
    def stop_test(self, test_id: str):
        """Stop a running test"""
        if test_id in self.active_tests:
            self.active_tests[test_id]['status'] = 'stopped'
            self.is_running = False
            self.logger.info(f"Test {test_id} stopped by user")
            return True
        return False
    
    def get_test_status(self, test_id: str) -> Optional[Dict]:
        """Get status of a test"""
        return self.active_tests.get(test_id)
    
    def get_all_tests(self) -> Dict:
        """Get all active tests"""
        return self.active_tests