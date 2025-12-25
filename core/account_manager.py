# -*- coding: utf-8 -*-
"""
ACCOUNT MANAGER - TIKTOK ACCOUNT HANDLING
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
import random
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from config import Config
from utils.logger import Logger

class AccountManager:
    def __init__(self):
        self.accounts_file = Config.ACCOUNTS_FILE
        self.accounts = self.load_accounts()
        self.logger = Logger("account_manager")
        
    def load_accounts(self) -> List[Dict]:
        """Load accounts from JSON file"""
        try:
            if self.accounts_file.exists():
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('accounts', [])
        except Exception as e:
            self.logger.error(f"Failed to load accounts: {e}")
        
        return []
    
    def save_accounts(self):
        """Save accounts to JSON file"""
        try:
            data = {'accounts': self.accounts}
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save accounts: {e}")
            return False
    
    def add_account(self, username: str, password: str, email: str = None, phone: str = None) -> bool:
        """Add a new TikTok account"""
        # Check if account already exists
        for acc in self.accounts:
            if acc['username'] == username:
                self.logger.warning(f"Account {username} already exists")
                return False
        
        new_account = {
            'id': len(self.accounts) + 1,
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,
            'status': 'active',
            'views_sent': 0,
            'last_used': None,
            'created_at': datetime.now().isoformat(),
            'notes': ''
        }
        
        self.accounts.append(new_account)
        self.save_accounts()
        self.logger.info(f"Account {username} added successfully")
        return True
    
    def remove_account(self, username: str) -> bool:
        """Remove a TikTok account"""
        for i, acc in enumerate(self.accounts):
            if acc['username'] == username:
                self.accounts.pop(i)
                self.save_accounts()
                self.logger.info(f"Account {username} removed")
                return True
        return False
    
    def update_account_status(self, username: str, status: str) -> bool:
        """Update account status (active, banned, limited, etc.)"""
        for acc in self.accounts:
            if acc['username'] == username:
                acc['status'] = status
                acc['last_updated'] = datetime.now().isoformat()
                self.save_accounts()
                self.logger.info(f"Account {username} status updated to {status}")
                return True
        return False
    
    def update_account_usage(self, username: str, views_sent: int = 1):
        """Update account usage statistics"""
        for acc in self.accounts:
            if acc['username'] == username:
                acc['views_sent'] += views_sent
                acc['last_used'] = datetime.now().isoformat()
                self.save_accounts()
                break
    
    def get_active_accounts(self) -> List[Dict]:
        """Get all active accounts"""
        return [acc for acc in self.accounts if acc['status'] == 'active']
    
    def get_account(self, username: str) -> Optional[Dict]:
        """Get specific account by username"""
        for acc in self.accounts:
            if acc['username'] == username:
                return acc
        return None
    
    def get_account_by_id(self, account_id: int) -> Optional[Dict]:
        """Get account by ID"""
        for acc in self.accounts:
            if acc['id'] == account_id:
                return acc
        return None
    
    def get_random_account(self) -> Optional[Dict]:
        """Get a random active account"""
        active = self.get_active_accounts()
        if active:
            return random.choice(active)
        return None
    
    def rotate_account(self, current_account: Dict = None) -> Dict:
        """Rotate to next available account"""
        active = self.get_active_accounts()
        if not active:
            return None
        
        if current_account:
            # Find next account
            current_index = next((i for i, acc in enumerate(active) 
                                if acc['username'] == current_account['username']), -1)
            next_index = (current_index + 1) % len(active)
            return active[next_index]
        else:
            # Return least recently used
            active.sort(key=lambda x: x.get('last_used', ''))
            return active[0]
    
    def import_accounts_from_file(self, file_path: str, format_type: str = 'json') -> int:
        """Import accounts from file"""
        imported = 0
        
        try:
            if format_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    accounts_to_import = data.get('accounts', [])
            elif format_type == 'txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    accounts_to_import = []
                    for line in f:
                        if ':' in line:
                            username, password = line.strip().split(':', 1)
                            accounts_to_import.append({
                                'username': username,
                                'password': password
                            })
            else:
                self.logger.error(f"Unsupported format: {format_type}")
                return 0
            
            for acc_data in accounts_to_import:
                username = acc_data.get('username')
                password = acc_data.get('password')
                
                if username and password:
                    if self.add_account(username, password):
                        imported += 1
            
            self.logger.info(f"Imported {imported} accounts from {file_path}")
            return imported
            
        except Exception as e:
            self.logger.error(f"Failed to import accounts: {e}")
            return 0
    
    def export_accounts_to_file(self, file_path: str, format_type: str = 'json') -> bool:
        """Export accounts to file"""
        try:
            if format_type == 'json':
                data = {'accounts': self.accounts}
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format_type == 'txt':
                with open(file_path, 'w', encoding='utf-8') as f:
                    for acc in self.accounts:
                        f.write(f"{acc['username']}:{acc['password']}\n")
            else:
                self.logger.error(f"Unsupported format: {format_type}")
                return False
            
            self.logger.info(f"Exported {len(self.accounts)} accounts to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export accounts: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get account statistics"""
        total = len(self.accounts)
        active = len(self.get_active_accounts())
        banned = len([acc for acc in self.accounts if acc['status'] == 'banned'])
        limited = len([acc for acc in self.accounts if acc['status'] == 'limited'])
        
        total_views = sum(acc.get('views_sent', 0) for acc in self.accounts)
        
        return {
            'total_accounts': total,
            'active_accounts': active,
            'banned_accounts': banned,
            'limited_accounts': limited,
            'total_views_sent': total_views,
            'avg_views_per_account': total_views / total if total > 0 else 0
        }