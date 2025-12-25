# -*- coding: utf-8 -*-
"""
ERROR HANDLER - EXCEPTION HANDLING AND ERROR MANAGEMENT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import sys
import traceback
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from utils.logger import Logger

class ErrorHandler:
    def __init__(self):
        self.logger = Logger("error_handler")
        self.error_log = []
        self.max_error_log = 1000
        
        # Error categories and their handling
        self.error_categories = {
            'network': {
                'retry': True,
                'max_retries': 3,
                'delay': 5,
                'notify': True
            },
            'authentication': {
                'retry': False,
                'notify': True,
                'severity': 'high'
            },
            'database': {
                'retry': True,
                'max_retries': 2,
                'delay': 10,
                'notify': True,
                'severity': 'critical'
            },
            'validation': {
                'retry': False,
                'notify': False,
                'severity': 'low'
            },
            'system': {
                'retry': False,
                'notify': True,
                'severity': 'critical'
            },
            'unknown': {
                'retry': False,
                'notify': True,
                'severity': 'medium'
            }
        }
    
    def handle_exception(self, exception: Exception, 
                        context: str = '', 
                        category: str = 'unknown',
                        raise_again: bool = False) -> Dict:
        """Handle exception with logging and recovery"""
        try:
            # Get exception details
            exc_type = type(exception).__name__
            exc_message = str(exception)
            exc_traceback = traceback.format_exc()
            
            # Create error record
            error_record = {
                'id': self._generate_error_id(),
                'timestamp': datetime.now().isoformat(),
                'type': exc_type,
                'message': exc_message,
                'category': category,
                'context': context,
                'traceback': exc_traceback,
                'handled': False,
                'recovered': False
            }
            
            # Log error
            self._log_error(error_record)
            
            # Store in error log
            self.error_log.append(error_record)
            if len(self.error_log) > self.max_error_log:
                self.error_log = self.error_log[-self.max_error_log:]
            
            # Get error handling configuration
            config = self.error_categories.get(category, self.error_categories['unknown'])
            
            # Attempt recovery based on category
            if config.get('retry', False):
                recovery_result = self._attempt_recovery(exception, context, config)
                error_record['recovered'] = recovery_result['success']
                error_record['recovery_attempts'] = recovery_result['attempts']
            
            # Determine if notification is needed
            if config.get('notify', False):
                self._send_notification(error_record, config.get('severity', 'medium'))
            
            # Mark as handled
            error_record['handled'] = True
            
            self.logger.info(f"Exception handled: {exc_type} in {context}")
            
            # Return error record
            return error_record
            
        except Exception as e:
            # If error handler itself fails
            self.logger.critical(f"Error handler failed: {e}")
            return {
                'id': 'ERROR_HANDLER_FAILED',
                'timestamp': datetime.now().isoformat(),
                'type': 'ErrorHandlerException',
                'message': str(e),
                'category': 'system',
                'context': 'error_handler',
                'handled': False,
                'recovered': False
            }
        finally:
            if raise_again:
                raise exception
    
    def _generate_error_id(self) -> str:
        """Generate unique error ID"""
        import hashlib
        import time
        import random
        
        data = f"{time.time()}{random.random()}"
        return hashlib.md5(data.encode()).hexdigest()[:8].upper()
    
    def _log_error(self, error_record: Dict):
        """Log error with appropriate level"""
        log_message = (
            f"ERROR [{error_record['category']}] "
            f"{error_record['type']}: {error_record['message']} "
            f"Context: {error_record['context']}"
        )
        
        # Map category to log level
        log_levels = {
            'critical': logging.CRITICAL,
            'high': logging.ERROR,
            'medium': logging.WARNING,
            'low': logging.INFO
        }
        
        category_config = self.error_categories.get(
            error_record['category'], 
            self.error_categories['unknown']
        )
        
        severity = category_config.get('severity', 'medium')
        level = log_levels.get(severity, logging.ERROR)
        
        self.logger.logger.log(level, log_message)
        
        # Log traceback at debug level
        self.logger.debug(f"Traceback: {error_record['traceback']}")
    
    def _attempt_recovery(self, exception: Exception, 
                         context: str, config: Dict) -> Dict:
        """Attempt to recover from error"""
        max_retries = config.get('max_retries', 3)
        delay = config.get('delay', 5)
        
        attempts = 0
        success = False
        
        self.logger.info(f"Attempting recovery for {type(exception).__name__} in {context}")
        
        while attempts < max_retries and not success:
            attempts += 1
            
            try:
                # Recovery logic based on error type
                if 'network' in context.lower() or 'connection' in str(exception).lower():
                    success = self._recover_network_error()
                elif 'database' in context.lower():
                    success = self._recover_database_error()
                else:
                    # Generic recovery: wait and retry
                    import time
                    time.sleep(delay * attempts)  # Exponential backoff
                    success = True
                
                if success:
                    self.logger.info(f"Reco successful after {attempts} attempt(s)")
                else:
                    self.logger.warning(f"Recovery attempt {attempts} failed")
                    
            except Exception as recovery_error:
                self.logger.error(f"Recovery attempt {attempts} caused error: {recovery_error}")
        
        return {
            'success': success,
            'attempts': attempts
        }
    
    def _recover_network_error(self) -> bool:
        """Attempt to recover from network error"""
        try:
            # Check network connectivity
            import socket
            import time
            
            # Try to connect to Google DNS
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            
            self.logger.info("Network connectivity restored")
            return True
            
        except:
            self.logger.warning("Network connectivity still unavailable")
            return False
    
    def _recover_database_error(self) -> bool:
        """Attempt to recover from database error"""
        try:
            # Try to reinitialize database connection
            from database.database import Database
            db = Database()
            
            # Test connection
            conn = db.get_connection()
            conn.close()
            
            self.logger.info("Database connection restored")
            return True
            
        except Exception as e:
            self.logger.error(f"Database recovery failed: {e}")
            return False
    
    def _send_notification(self, error_record: Dict, severity: str):
        """Send error notification"""
        try:
            notification = self._format_notification(error_record, severity)
            
            # In a real implementation, this would send:
            # - Email to admin
            # - Telegram message
            # - Slack notification
            # - SMS alert
            
            # For now, just log it
            self.logger.critical(f"ERROR NOTIFICATION: {notification}")
            
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
    
    def _format_notification(self, error_record: Dict, severity: str) -> str:
        """Format error notification"""
        return (
            f"🚨 ERROR ALERT - Severity: {severity.upper()}\n"
            f"──────────────────────────────\n"
            f"ID: {error_record['id']}\n"
            f"Time: {error_record['timestamp']}\n"
            f"Type: {error_record['type']}\n"
            f"Category: {error_record['category']}\n"
            f"Context: {error_record['context']}\n"
            f"Message: {error_record['message'][:200]}\n"
            f"──────────────────────────────\n"
            f"Action Required: {'YES' if severity in ['critical', 'high'] else 'NO'}"
        )
    
    def get_error_stats(self, hours: int = 24) -> Dict:
        """Get error statistics"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        recent_errors = [
            e for e in self.error_log 
            if datetime.fromisoformat(e['timestamp']).timestamp() > cutoff
        ]
        
        stats = {
            'total_errors': len(recent_errors),
            'by_category': {},
            'by_type': {},
            'recovery_rate': 0,
            'most_common_error': None,
            'most_common_category': None
        }
        
        if recent_errors:
            # Count by category
            for error in recent_errors:
                category = error['category']
                stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Count by type
            for error in recent_errors:
                error_type = error['type']
                stats['by_type'][error_type] = stats['by_type'].get(error_type, 0) + 1
            
            # Calculate recovery rate
            recovered = sum(1 for e in recent_errors if e.get('recovered', False))
            stats['recovery_rate'] = (recovered / len(recent_errors)) * 100
            
            # Find most common
            if stats['by_category']:
                stats['most_common_category'] = max(stats['by_category'].items(), key=lambda x: x[1])[0]
            
            if stats['by_type']:
                stats['most_common_error'] = max(stats['by_type'].items(), key=lambda x: x[1])[0]
        
        return stats
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """Get recent errors"""
        return self.error_log[-limit:] if self.error_log else []
    
    def clear_error_log(self, days_old: int = 7):
        """Clear old error logs"""
        cutoff = datetime.now().timestamp() - (days_old * 86400)
        
        old_count = len(self.error_log)
        self.error_log = [
            e for e in self.error_log 
            if datetime.fromisoformat(e['timestamp']).timestamp() > cutoff
        ]
        removed = old_count - len(self.error_log)
        
        if removed > 0:
            self.logger.info(f"Cleared {removed} old error logs")
    
    def create_error_report(self, hours: int = 24) -> Dict:
        """Create detailed error report"""
        stats = self.get_error_stats(hours)
        recent_errors = self.get_recent_errors(20)
        
        report = {
            'report_id': self._generate_error_id(),
            'generated_at': datetime.now().isoformat(),
            'period_hours': hours,
            'summary': stats,
            'recent_errors': recent_errors,
            'recommendations': self._generate_recommendations(stats),
            'system_health': self._assess_system_health(stats)
        }
        
        return report
    
    def _generate_recommendations(self, stats: Dict) -> List[str]:
        """Generate recommendations based on error statistics"""
        recommendations = []
        
        total_errors = stats.get('total_errors', 0)
        recovery_rate = stats.get('recovery_rate', 0)
        
        if total_errors > 50:
            recommendations.append("High error rate detected. Review system stability.")
        
        if recovery_rate < 50:
            recommendations.append("Low recovery rate. Improve error handling mechanisms.")
        
        network_errors = stats.get('by_category', {}).get('network', 0)
        if network_errors > 10:
            recommendations.append("Frequent network errors. Check connectivity and proxies.")
        
        database_errors = stats.get('by_category', {}).get('database', 0)
        if database_errors > 5:
            recommendations.append("Database errors occurring. Verify database connection and schema.")
        
        if not recommendations:
            recommendations.append("System error rate is within acceptable limits.")
        
        return recommendations
    
    def _assess_system_health(self, stats: Dict) -> str:
        """Assess system health based on errors"""
        total_errors = stats.get('total_errors', 0)
        recovery_rate = stats.get('recovery_rate', 0)
        
        if total_errors == 0:
            return "excellent"
        elif total_errors < 10 and recovery_rate > 80:
            return "good"
        elif total_errors < 50 and recovery_rate > 50:
            return "fair"
        elif total_errors < 100:
            return "poor"
        else:
            return "critical"
    
    def wrap_function(self, func: Callable, 
                     context: str = '', 
                     category: str = 'unknown') -> Callable:
        """Wrap function with error handling"""
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_record = self.handle_exception(e, context, category)
                
                # Return error information instead of raising
                return {
                    'error': True,
                    'error_id': error_record['id'],
                    'message': str(e),
                    'context': context
                }
        
        return wrapped
    
    def retry_on_error(self, func: Callable, 
                      max_attempts: int = 3, 
                      delay: float = 1.0,
                      context: str = '',
                      category: str = 'unknown') -> Callable:
        """Wrap function with retry logic"""
        def wrapped(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        # Last attempt, handle error
                        error_record = self.handle_exception(e, context, category)
                        raise e
                    
                    # Wait before retry
                    import time
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            
            # Should not reach here
            return None
        
        return wrapped