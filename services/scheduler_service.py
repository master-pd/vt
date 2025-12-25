# -*- coding: utf-8 -*-
"""
SCHEDULER SERVICE - TASK SCHEDULING AND AUTOMATION
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Callable
from utils.logger import Logger

class SchedulerService:
    def __init__(self):
        self.logger = Logger("scheduler")
        self.scheduler = schedule.Scheduler()
        self.running = False
        self.scheduler_thread = None
        self.tasks = {}
        
        # Default scheduled tasks
        self._setup_default_tasks()
    
    def _setup_default_tasks(self):
        """Setup default scheduled tasks"""
        # Daily maintenance at 2 AM
        self.add_task(
            task_id="daily_maintenance",
            func=self._daily_maintenance,
            schedule_time="02:00",
            description="Daily system maintenance"
        )
        
        # Proxy check every 6 hours
        self.add_task(
            task_id="proxy_check",
            func=self._check_proxies,
            schedule_time="00:00",
            interval=6,  # hours
            description="Check proxy status"
        )
        
        # Account status check every 12 hours
        self.add_task(
            task_id="account_check",
            func=self._check_accounts,
            schedule_time="06:00",
            interval=12,  # hours
            description="Check account status"
        )
        
        # Report generation at midnight
        self.add_task(
            task_id="daily_report",
            func=self._generate_daily_report,
            schedule_time="00:00",
            description="Generate daily report"
        )
        
        # Data cleanup every Sunday at 3 AM
        self.add_task(
            task_id="data_cleanup",
            func=self._cleanup_old_data,
            schedule_time="03:00",
            days_of_week="sunday",
            description="Cleanup old data"
        )
    
    def add_task(self, task_id: str, func: Callable, schedule_time: str = None,
                 interval: int = None, unit: str = 'hours', days_of_week: str = None,
                 description: str = "") -> bool:
        """Add a scheduled task"""
        if task_id in self.tasks:
            self.logger.warning(f"Task {task_id} already exists")
            return False
        
        task = {
            'id': task_id,
            'func': func,
            'schedule_time': schedule_time,
            'interval': interval,
            'unit': unit,
            'days_of_week': days_of_week,
            'description': description,
            'last_run': None,
            'next_run': None,
            'run_count': 0,
            'enabled': True
        }
        
        # Schedule the task
        job = self._schedule_task(task)
        if job:
            task['job'] = job
            self.tasks[task_id] = task
            
            # Calculate next run
            if hasattr(job, 'next_run'):
                task['next_run'] = job.next_run
            
            self.logger.info(f"Task scheduled: {task_id} - {description}")
            return True
        
        return False
    
    def _schedule_task(self, task: Dict):
        """Schedule a task using schedule library"""
        try:
            if task['interval']:
                # Interval-based task
                if task['unit'] == 'seconds':
                    job = self.scheduler.every(task['interval']).seconds.do(
                        self._wrap_task, task['id']
                    )
                elif task['unit'] == 'minutes':
                    job = self.scheduler.every(task['interval']).minutes.do(
                        self._wrap_task, task['id']
                    )
                elif task['unit'] == 'hours':
                    job = self.scheduler.every(task['interval']).hours.do(
                        self._wrap_task, task['id']
                    )
                elif task['unit'] == 'days':
                    job = self.scheduler.every(task['interval']).days.do(
                        self._wrap_task, task['id']
                    )
                else:
                    self.logger.error(f"Invalid unit for task {task['id']}: {task['unit']}")
                    return None
            
            elif task['schedule_time']:
                # Time-based task
                if task['days_of_week']:
                    # Specific day of week
                    day_method = getattr(self.scheduler.every(), task['days_of_week'])
                    job = day_method.at(task['schedule_time']).do(
                        self._wrap_task, task['id']
                    )
                else:
                    # Daily at specific time
                    job = self.scheduler.every().day.at(task['schedule_time']).do(
                        self._wrap_task, task['id']
                    )
            
            else:
                self.logger.error(f"Task {task['id']} has no schedule specified")
                return None
            
            return job
            
        except Exception as e:
            self.logger.error(f"Failed to schedule task {task['id']}: {e}")
            return None
    
    def _wrap_task(self, task_id: str):
        """Wrapper function to execute task with logging"""
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return
        
        task = self.tasks[task_id]
        
        if not task['enabled']:
            self.logger.debug(f"Task {task_id} is disabled, skipping")
            return
        
        self.logger.info(f"Starting task: {task_id} - {task['description']}")
        start_time = time.time()
        
        try:
            # Execute the task
            result = task['func']()
            task['last_run'] = datetime.now()
            task['run_count'] += 1
            
            # Update next run time
            if task['job'] and hasattr(task['job'], 'next_run'):
                task['next_run'] = task['job'].next_run
            
            duration = time.time() - start_time
            self.logger.info(f"Task completed: {task_id} in {duration:.2f}s - Result: {result}")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"Task failed: {task_id} after {duration:.2f}s - Error: {e}")
            return None
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a scheduled task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        # Cancel the job
        if 'job' in task:
            self.scheduler.cancel_job(task['job'])
        
        del self.tasks[task_id]
        self.logger.info(f"Task removed: {task_id}")
        
        return True
    
    def enable_task(self, task_id: str) -> bool:
        """Enable a task"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id]['enabled'] = True
        self.logger.info(f"Task enabled: {task_id}")
        
        return True
    
    def disable_task(self, task_id: str) -> bool:
        """Disable a task"""
        if task_id not in self.tasks:
            return False
        
        self.tasks[task_id]['enabled'] = False
        self.logger.info(f"Task disabled: {task_id}")
        
        return True
    
    def run_task_now(self, task_id: str):
        """Run a task immediately"""
        if task_id not in self.tasks:
            self.logger.error(f"Task {task_id} not found")
            return None
        
        task = self.tasks[task_id]
        self.logger.info(f"Manual execution: {task_id}")
        
        return task['func']()
    
    def get_task_status(self, task_id: str) -> Dict:
        """Get status of a task"""
        if task_id not in self.tasks:
            return {'error': 'Task not found'}
        
        task = self.tasks[task_id]
        
        return {
            'id': task_id,
            'description': task['description'],
            'enabled': task['enabled'],
            'last_run': task['last_run'].isoformat() if task['last_run'] else None,
            'next_run': task['next_run'].isoformat() if task['next_run'] else None,
            'run_count': task['run_count'],
            'schedule': {
                'time': task['schedule_time'],
                'interval': task['interval'],
                'unit': task['unit'],
                'days_of_week': task['days_of_week']
            }
        }
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all scheduled tasks"""
        tasks = []
        
        for task_id, task in self.tasks.items():
            tasks.append(self.get_task_status(task_id))
        
        return tasks
    
    def start(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.running = True
        
        def run_scheduler():
            self.logger.info("Scheduler started")
            
            while self.running:
                try:
                    self.scheduler.run_pending()
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"Scheduler error: {e}")
                    time.sleep(5)
            
            self.logger.info("Scheduler stopped")
        
        # Start scheduler in background thread
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("Scheduler service started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
            self.scheduler_thread = None
        
        self.logger.info("Scheduler service stopped")
    
    # Default task implementations
    def _daily_maintenance(self) -> str:
        """Perform daily maintenance tasks"""
        self.logger.info("Running daily maintenance")
        
        # Tasks to perform:
        # 1. Check system health
        # 2. Cleanup temporary files
        # 3. Optimize database
        # 4. Update statistics
        
        return "Daily maintenance completed"
    
    def _check_proxies(self) -> str:
        """Check and update proxy status"""
        self.logger.info("Checking proxy status")
        
        # Import here to avoid circular imports
        from core.proxy_handler import ProxyHandler
        proxy_handler = ProxyHandler()
        
        result = proxy_handler.check_all_proxies()
        
        return f"Proxy check: {result['working']}/{result['total']} working"
    
    def _check_accounts(self) -> str:
        """Check and update account status"""
        self.logger.info("Checking account status")
        
        # Import here to avoid circular imports
        from core.account_manager import AccountManager
        account_manager = AccountManager()
        
        # Check account status (would implement actual checking)
        accounts = account_manager.get_active_accounts()
        
        return f"Account check: {len(accounts)} active accounts"
    
    def _generate_daily_report(self) -> str:
        """Generate daily report"""
        self.logger.info("Generating daily report")
        
        # Import here to avoid circular imports
        from services.report_service import ReportService
        report_service = ReportService()
        
        report = report_service.generate_daily_report()
        
        return f"Daily report generated: {len(report.get('files_generated', []))} files"
    
    def _cleanup_old_data(self) -> str:
        """Cleanup old data"""
        self.logger.info("Cleaning up old data")
        
        # Import here to avoid circular imports
        from database.json_db import JSONDatabase
        json_db = JSONDatabase()
        
        json_db.cleanup_old_data(days=30)
        
        return "Old data cleanup completed"
    
    def schedule_one_time_task(self, task_id: str, func: Callable, 
                               run_at: datetime, description: str = "") -> bool:
        """Schedule a one-time task at specific datetime"""
        # Calculate delay in seconds
        now = datetime.now()
        if run_at <= now:
            self.logger.warning(f"Task {task_id} scheduled time is in the past")
            return False
        
        delay = (run_at - now).total_seconds()
        
        task = {
            'id': task_id,
            'func': func,
            'description': description,
            'run_at': run_at,
            'scheduled': False
        }
        
        # Schedule using threading Timer
        timer = threading.Timer(delay, self._execute_one_time_task, args=[task_id])
        timer.start()
        
        task['timer'] = timer
        self.tasks[task_id] = task
        
        self.logger.info(f"One-time task scheduled: {task_id} at {run_at}")
        return True
    
    def _execute_one_time_task(self, task_id: str):
        """Execute one-time task"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        self.logger.info(f"Executing one-time task: {task_id}")
        
        try:
            result = task['func']()
            self.logger.info(f"One-time task completed: {task_id} - Result: {result}")
            
            # Remove from tasks after execution
            del self.tasks[task_id]
            
            return result
            
        except Exception as e:
            self.logger.error(f"One-time task failed: {task_id} - Error: {e}")
            del self.tasks[task_id]
            return None
    
    def get_upcoming_tasks(self, limit: int = 10) -> List[Dict]:
        """Get upcoming tasks"""
        upcoming = []
        
        for task_id, task in self.tasks.items():
            if task.get('next_run'):
                upcoming.append({
                    'id': task_id,
                    'description': task['description'],
                    'next_run': task['next_run']
                })
        
        # Sort by next run time
        upcoming.sort(key=lambda x: x['next_run'])
        
        return upcoming[:limit]