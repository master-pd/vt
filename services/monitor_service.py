# -*- coding: utf-8 -*-
"""
MONITOR SERVICE - SYSTEM MONITORING AND ALERTS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from utils.logger import Logger

class MonitorService:
    def __init__(self):
        self.logger = Logger("monitor")
        self.metrics_history = []
        self.max_history_size = 1000
        self.alerts = []
        self.alert_rules = self._setup_alert_rules()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time_ms': 1000,
            'error_rate': 5.0,
            'queue_size': 50,
            'success_rate': 60.0
        }
    
    def _setup_alert_rules(self) -> List[Dict]:
        """Setup alert rules"""
        return [
            {
                'id': 'high_cpu',
                'metric': 'cpu_percent',
                'condition': '>',
                'threshold': 80,
                'severity': 'warning',
                'message': 'CPU usage is high',
                'cooldown': 300  # 5 minutes
            },
            {
                'id': 'high_memory',
                'metric': 'memory_percent',
                'condition': '>',
                'threshold': 85,
                'severity': 'warning',
                'message': 'Memory usage is high',
                'cooldown': 300
            },
            {
                'id': 'low_success_rate',
                'metric': 'success_rate',
                'condition': '<',
                'threshold': 60,
                'severity': 'critical',
                'message': 'Success rate is below threshold',
                'cooldown': 600
            },
            {
                'id': 'high_error_rate',
                'metric': 'error_rate',
                'condition': '>',
                'threshold': 5,
                'severity': 'critical',
                'message': 'Error rate is high',
                'cooldown': 300
            },
            {
                'id': 'queue_backlog',
                'metric': 'queue_size',
                'condition': '>',
                'threshold': 50,
                'severity': 'warning',
                'message': 'Queue is getting large',
                'cooldown': 300
            }
        ]
    
    def collect_metrics(self) -> Dict:
        """Collect system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': self._get_system_metrics(),
            'performance': self._get_performance_metrics(),
            'application': self._get_application_metrics()
        }
        
        # Store in history
        self.metrics_history.append(metrics)
        
        # Trim history if too large
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
        
        # Check for alerts
        self._check_alerts(metrics)
        
        return metrics
    
    def _get_system_metrics(self) -> Dict:
        """Get system-level metrics"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network
            net_io = psutil.net_io_counters()
            
            # Processes
            process_count = len(psutil.pids())
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency_mhz': cpu_freq.current if cpu_freq else None
                },
                'memory': {
                    'percent': memory.percent,
                    'total_gb': memory.total / (1024**3),
                    'available_gb': memory.available / (1024**3),
                    'used_gb': memory.used / (1024**3)
                },
                'swap': {
                    'percent': swap.percent,
                    'total_gb': swap.total / (1024**3),
                    'used_gb': swap.used / (1024**3)
                },
                'disk': {
                    'percent': disk.percent,
                    'total_gb': disk.total / (1024**3),
                    'used_gb': disk.used / (1024**3),
                    'free_gb': disk.free / (1024**3),
                    'read_mb': disk_io.read_bytes / (1024**2) if disk_io else 0,
                    'write_mb': disk_io.write_bytes / (1024**2) if disk_io else 0
                },
                'network': {
                    'sent_mb': net_io.bytes_sent / (1024**2),
                    'received_mb': net_io.bytes_recv / (1024**2)
                },
                'processes': process_count
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def _get_performance_metrics(self) -> Dict:
        """Get application performance metrics"""
        # Import here to avoid circular imports
        from database.database import Database
        from core.view_engine import ViewEngine
        
        try:
            db = Database()
            view_engine = ViewEngine()
            
            # Get database statistics
            db_stats = db.get_statistics()
            
            # Get view engine status
            active_tests = view_engine.get_all_tests()
            
            # Get queue status from JSON database
            from database.json_db import JSONDatabase
            json_db = JSONDatabase()
            queue = json_db.get_queue('pending')
            
            return {
                'tests': {
                    'total': db_stats.get('total_tests', 0),
                    'today': db_stats.get('today_tests', 0),
                    'active': len(active_tests),
                    'success_rate': db_stats.get('success_rate', 0)
                },
                'views': {
                    'total': db_stats.get('total_views', 0),
                    'today': db_stats.get('today_views', 0),
                    'sent_per_minute': self._calculate_views_per_minute()
                },
                'queue': {
                    'size': len(queue),
                    'pending': len([t for t in queue if t.get('status') == 'pending']),
                    'processing': len([t for t in queue if t.get('status') == 'processing'])
                },
                'accounts': {
                    'total': 0,  # Would get from account manager
                    'active': 0,
                    'banned': 0
                },
                'proxies': {
                    'total': 0,  # Would get from proxy handler
                    'active': 0,
                    'inactive': 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {e}")
            return {}
    
    def _get_application_metrics(self) -> Dict:
        """Get application-specific metrics"""
        # Import services
        from services.analytics_service import AnalyticsService
        
        try:
            analytics = AnalyticsService()
            performance = analytics.get_system_performance()
            
            return {
                'uptime': performance.get('system_uptime', ''),
                'response_time_ms': performance.get('avg_response_time', 0),
                'error_rate': performance.get('error_rate', 0),
                'requests_per_minute': performance.get('requests_per_minute', 0),
                'system_load': performance.get('system_load', 0),
                'account_health': performance.get('account_health', 0),
                'proxy_health': performance.get('proxy_health', 0),
                'efficiency_score': self._calculate_efficiency_score()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting application metrics: {e}")
            return {}
    
    def _calculate_views_per_minute(self) -> float:
        """Calculate views sent per minute"""
        if len(self.metrics_history) < 2:
            return 0
        
        # Get views from last 5 minutes of metrics
        five_min_ago = datetime.now() - timedelta(minutes=5)
        recent_metrics = [
            m for m in self.metrics_history 
            if datetime.fromisoformat(m['timestamp']) > five_min_ago
        ]
        
        if len(recent_metrics) < 2:
            return 0
        
        # Calculate average views per minute
        total_views = 0
        for metrics in recent_metrics:
            total_views += metrics.get('performance', {}).get('views', {}).get('sent_per_minute', 0)
        
        return total_views / len(recent_metrics) if recent_metrics else 0
    
    def _calculate_efficiency_score(self) -> float:
        """Calculate overall system efficiency score"""
        # This would calculate based on multiple factors
        # For now, return a simulated score
        
        metrics = self.get_current_metrics()
        
        cpu_score = 100 - min(100, metrics['system']['cpu']['percent'])
        memory_score = 100 - min(100, metrics['system']['memory']['percent'])
        success_score = metrics['performance']['tests']['success_rate']
        
        efficiency = (cpu_score * 0.3) + (memory_score * 0.3) + (success_score * 0.4)
        
        return round(efficiency, 1)
    
    def _check_alerts(self, metrics: Dict):
        """Check metrics against alert rules"""
        current_time = time.time()
        
        for rule in self.alert_rules:
            # Get metric value
            metric_value = self._get_metric_value(metrics, rule['metric'])
            if metric_value is None:
                continue
            
            # Check condition
            should_alert = False
            if rule['condition'] == '>':
                should_alert = metric_value > rule['threshold']
            elif rule['condition'] == '<':
                should_alert = metric_value < rule['threshold']
            elif rule['condition'] == '==':
                should_alert = metric_value == rule['threshold']
            elif rule['condition'] == '!=':
                should_alert = metric_value != rule['threshold']
            
            if should_alert:
                # Check cooldown
                last_alert = self._get_last_alert(rule['id'])
                if last_alert and (current_time - last_alert['timestamp']) < rule['cooldown']:
                    continue
                
                # Create alert
                alert = {
                    'id': rule['id'],
                    'severity': rule['severity'],
                    'message': rule['message'],
                    'metric': rule['metric'],
                    'value': metric_value,
                    'threshold': rule['threshold'],
                    'timestamp': current_time,
                    'acknowledged': False
                }
                
                self.alerts.append(alert)
                self.logger.warning(f"Alert triggered: {rule['message']} ({metric_value})")
                
                # Send notification
                self._send_alert_notification(alert)
    
    def _get_metric_value(self, metrics: Dict, metric_path: str):
        """Get metric value from nested dictionary using dot notation"""
        try:
            parts = metric_path.split('.')
            value = metrics
            
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return None
            
            return value if isinstance(value, (int, float)) else None
            
        except:
            return None
    
    def _get_last_alert(self, alert_id: str) -> Optional[Dict]:
        """Get last alert for specific rule"""
        for alert in reversed(self.alerts):
            if alert['id'] == alert_id:
                return alert
        return None
    
    def _send_alert_notification(self, alert: Dict):
        """Send alert notification"""
        # In a real implementation, this would send:
        # - Email
        # - Telegram message
        # - SMS
        # - Webhook
        
        # For now, just log it
        notification_message = (
            f"🚨 ALERT: {alert['message']}\n"
            f"Severity: {alert['severity'].upper()}\n"
            f"Metric: {alert['metric']} = {alert['value']}\n"
            f"Threshold: {alert['threshold']}\n"
            f"Time: {datetime.fromtimestamp(alert['timestamp'])}"
        )
        
        self.logger.critical(notification_message)
        
        # Would also send to Telegram bot if configured
        # await telegram_bot.send_alert(notification_message)
    
    def get_current_metrics(self) -> Dict:
        """Get current metrics (collects if not recent)"""
        if not self.metrics_history:
            return self.collect_metrics()
        
        last_metric = self.metrics_history[-1]
        last_time = datetime.fromisoformat(last_metric['timestamp'])
        
        # If last metric is more than 30 seconds old, collect new one
        if (datetime.now() - last_time).total_seconds() > 30:
            return self.collect_metrics()
        
        return last_metric
    
    def get_metrics_history(self, minutes: int = 60) -> List[Dict]:
        """Get metrics history for specified minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        
        history = []
        for metric in self.metrics_history:
            metric_time = datetime.fromisoformat(metric['timestamp'])
            if metric_time > cutoff:
                history.append(metric)
        
        return history
    
    def get_active_alerts(self, acknowledged: bool = None) -> List[Dict]:
        """Get active alerts"""
        if acknowledged is None:
            return self.alerts
        
        return [a for a in self.alerts if a['acknowledged'] == acknowledged]
    
    def acknowledge_alert(self, alert_id: str, acknowledge_all: bool = False) -> bool:
        """Acknowledge an alert"""
        if acknowledge_all:
            for alert in self.alerts:
                if not alert['acknowledged']:
                    alert['acknowledged'] = True
            self.logger.info("All alerts acknowledged")
            return True
        
        for alert in self.alerts:
            if alert['id'] == alert_id and not alert['acknowledged']:
                alert['acknowledged'] = True
                self.logger.info(f"Alert {alert_id} acknowledged")
                return True
        
        return False
    
    def clear_old_alerts(self, hours: int = 24):
        """Clear alerts older than specified hours"""
        cutoff = time.time() - (hours * 3600)
        
        old_count = len(self.alerts)
        self.alerts = [a for a in self.alerts if a['timestamp'] > cutoff]
        removed = old_count - len(self.alerts)
        
        if removed > 0:
            self.logger.info(f"Cleared {removed} old alerts")
    
    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        metrics = self.get_current_metrics()
        
        # Calculate health score (0-100)
        health_score = self._calculate_efficiency_score()
        
        # Determine status
        if health_score >= 80:
            status = 'healthy'
            status_emoji = '🟢'
        elif health_score >= 60:
            status = 'degraded'
            status_emoji = '🟡'
        else:
            status = 'unhealthy'
            status_emoji = '🔴'
        
        # Get active issues
        active_alerts = [a for a in self.alerts if not a['acknowledged']]
        critical_alerts = [a for a in active_alerts if a['severity'] == 'critical']
        
        return {
            'status': status,
            'status_emoji': status_emoji,
            'health_score': health_score,
            'timestamp': datetime.now().isoformat(),
            'active_alerts': len(active_alerts),
            'critical_alerts': len(critical_alerts),
            'metrics': {
                'cpu_percent': metrics['system']['cpu']['percent'],
                'memory_percent': metrics['system']['memory']['percent'],
                'success_rate': metrics['performance']['tests']['success_rate'],
                'queue_size': metrics['performance']['queue']['size']
            },
            'recommendations': self._generate_health_recommendations(metrics, active_alerts)
        }
    
    def _generate_health_recommendations(self, metrics: Dict, alerts: List[Dict]) -> List[str]:
        """Generate health recommendations"""
        recommendations = []
        
        cpu_percent = metrics['system']['cpu']['percent']
        memory_percent = metrics['system']['memory']['percent']
        success_rate = metrics['performance']['tests']['success_rate']
        queue_size = metrics['performance']['queue']['size']
        
        if cpu_percent > 70:
            recommendations.append("CPU usage is high. Consider optimizing resource usage or upgrading hardware.")
        
        if memory_percent > 75:
            recommendations.append("Memory usage is high. Consider increasing memory or optimizing memory usage.")
        
        if success_rate < 65:
            recommendations.append("Success rate is low. Check proxy and account health.")
        
        if queue_size > 20:
            recommendations.append("Queue is growing. Consider increasing processing capacity.")
        
        if not recommendations:
            recommendations.append("System is running optimally. No immediate action needed.")
        
        return recommendations
    
    def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring"""
        import threading
        
        def monitor_loop():
            self.logger.info(f"Monitoring started with {interval_seconds}s interval")
            
            while True:
                try:
                    self.collect_metrics()
                    time.sleep(interval_seconds)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
                    time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        self.logger.info("Monitor service started")