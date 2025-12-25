# -*- coding: utf-8 -*-
"""
JSON DATABASE - SIMPLE JSON-BASED STORAGE
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from config import Config
from utils.logger import Logger

class JSONDatabase:
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        self.data_dir.mkdir(exist_ok=True)
        self.logger = Logger("json_db")
        
        # Initialize JSON files
        self.files = {
            'accounts': Config.ACCOUNTS_FILE,
            'proxies': Config.PROXIES_FILE,
            'settings': self.data_dir / "settings.json",
            'statistics': self.data_dir / "statistics.json",
            'queue': self.data_dir / "queue.json"
        }
        
        self._init_files()
    
    def _init_files(self):
        """Initialize JSON files with default structure"""
        defaults = {
            'accounts': {'accounts': [], 'last_updated': None},
            'proxies': {'proxies': [], 'last_updated': None},
            'settings': {'app': {}, 'tiktok': {}, 'telegram': {}},
            'statistics': {'daily': {}, 'weekly': {}, 'monthly': {}},
            'queue': {'pending': [], 'processing': [], 'completed': []}
        }
        
        for name, filepath in self.files.items():
            if not filepath.exists():
                self._save_json(filepath, defaults[name])
                self.logger.info(f"Created {name} file: {filepath}")
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load {filepath}: {e}")
            return {}
    
    def _save_json(self, filepath: Path, data: Dict):
        """Save JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save {filepath}: {e}")
            return False
    
    # Account methods
    def get_accounts(self) -> List[Dict]:
        """Get all accounts"""
        data = self._load_json(self.files['accounts'])
        accounts = data.get('accounts', [])
        
        # Add timestamp if not present
        for acc in accounts:
            if 'last_used' not in acc:
                acc['last_used'] = None
            if 'created_at' not in acc:
                acc['created_at'] = datetime.now().isoformat()
        
        return accounts
    
    def save_accounts(self, accounts: List[Dict]):
        """Save accounts to JSON"""
        data = {
            'accounts': accounts,
            'last_updated': datetime.now().isoformat(),
            'total_accounts': len(accounts)
        }
        return self._save_json(self.files['accounts'], data)
    
    def update_account_usage(self, username: str):
        """Update account last used timestamp"""
        accounts = self.get_accounts()
        
        for acc in accounts:
            if acc['username'] == username:
                acc['last_used'] = datetime.now().isoformat()
                acc['views_sent'] = acc.get('views_sent', 0) + 1
                break
        
        self.save_accounts(accounts)
        return True
    
    # Proxy methods
    def get_proxies(self) -> List[Dict]:
        """Get all proxies"""
        data = self._load_json(self.files['proxies'])
        return data.get('proxies', [])
    
    def save_proxies(self, proxies: List[Dict]):
        """Save proxies to JSON"""
        data = {
            'proxies': proxies,
            'last_updated': datetime.now().isoformat(),
            'total_proxies': len(proxies)
        }
        return self._save_json(self.files['proxies'], data)
    
    # Settings methods
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        data = self._load_json(self.files['settings'])
        category_data = data.get(category, {})
        return category_data.get(key, default)
    
    def set_setting(self, category: str, key: str, value: Any):
        """Set a setting value"""
        data = self._load_json(self.files['settings'])
        
        if category not in data:
            data[category] = {}
        
        data[category][key] = value
        data['last_updated'] = datetime.now().isoformat()
        
        return self._save_json(self.files['settings'], data)
    
    # Statistics methods
    def record_statistic(self, metric: str, value: float, date: str = None):
        """Record a statistic"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        data = self._load_json(self.files['statistics'])
        
        if 'daily' not in data:
            data['daily'] = {}
        
        if date not in data['daily']:
            data['daily'][date] = {}
        
        data['daily'][date][metric] = value
        data['daily'][date]['timestamp'] = datetime.now().isoformat()
        
        return self._save_json(self.files['statistics'], data)
    
    def get_statistics(self, period: str = 'daily', date: str = None) -> Dict:
        """Get statistics for period"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        data = self._load_json(self.files['statistics'])
        period_data = data.get(period, {})
        
        if period == 'daily':
            return period_data.get(date, {})
        else:
            return period_data
    
    # Queue methods
    def add_to_queue(self, item: Dict, queue_type: str = 'pending'):
        """Add item to queue"""
        data = self._load_json(self.files['queue'])
        
        if queue_type not in data:
            data[queue_type] = []
        
        item['added_at'] = datetime.now().isoformat()
        item['queue_id'] = f"{queue_type}_{len(data[queue_type]) + 1}"
        
        data[queue_type].append(item)
        
        return self._save_json(self.files['queue'], data)
    
    def get_queue(self, queue_type: str = 'pending') -> List[Dict]:
        """Get items from queue"""
        data = self._load_json(self.files['queue'])
        return data.get(queue_type, [])
    
    def move_queue_item(self, queue_id: str, from_queue: str, to_queue: str):
        """Move item between queues"""
        data = self._load_json(self.files['queue'])
        
        if from_queue not in data or to_queue not in data:
            return False
        
        # Find and move item
        for i, item in enumerate(data[from_queue]):
            if item.get('queue_id') == queue_id:
                moved_item = data[from_queue].pop(i)
                moved_item['moved_at'] = datetime.now().isoformat()
                data[to_queue].append(moved_item)
                
                self._save_json(self.files['queue'], data)
                return True
        
        return False
    
    def cleanup_old_data(self, days: int = 30):
        """Cleanup old data from JSON files"""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 3600)
        
        # Clean statistics
        data = self._load_json(self.files['statistics'])
        if 'daily' in data:
            for date in list(data['daily'].keys()):
                try:
                    date_obj = datetime.strptime(date, '%Y-%m-%d')
                    if date_obj.timestamp() < cutoff_date:
                        del data['daily'][date]
                except:
                    pass
        
        self._save_json(self.files['statistics'], data)
        self.logger.info(f"Cleaned up data older than {days} days")