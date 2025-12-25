# -*- coding: utf-8 -*-
"""
PROXY HANDLER - PROXY ROTATION AND MANAGEMENT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
import random
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from config import Config
from utils.logger import Logger

class ProxyHandler:
    def __init__(self):
        self.proxies_file = Config.PROXIES_FILE
        self.proxies = self.load_proxies()
        self.logger = Logger("proxy_handler")
        self.current_proxy_index = 0
        
    def load_proxies(self) -> List[Dict]:
        """Load proxies from JSON file"""
        try:
            if self.proxies_file.exists():
                with open(self.proxies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('proxies', [])
        except Exception as e:
            self.logger.error(f"Failed to load proxies: {e}")
        
        return []
    
    def save_proxies(self):
        """Save proxies to JSON file"""
        try:
            data = {'proxies': self.proxies}
            with open(self.proxies_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save proxies: {e}")
            return False
    
    def add_proxy(self, proxy_string: str, proxy_type: str = 'http', 
                  country: str = None, speed: int = 0) -> bool:
        """Add a new proxy"""
        # Validate proxy format
        if not self._validate_proxy(proxy_string):
            self.logger.error(f"Invalid proxy format: {proxy_string}")
            return False
        
        # Check if proxy already exists
        for proxy in self.proxies:
            if proxy['proxy'] == proxy_string:
                self.logger.warning(f"Proxy {proxy_string} already exists")
                return False
        
        new_proxy = {
            'id': len(self.proxies) + 1,
            'proxy': proxy_string,
            'type': proxy_type,
            'country': country,
            'speed': speed,
            'last_used': None,
            'last_checked': None,
            'success_rate': 0,
            'is_active': True,
            'added_at': datetime.now().isoformat()
        }
        
        self.proxies.append(new_proxy)
        self.save_proxies()
        self.logger.info(f"Proxy added: {proxy_string}")
        return True
    
    def _validate_proxy(self, proxy_string: str) -> bool:
        """Validate proxy format"""
        if '://' in proxy_string:
            # Format: http://user:pass@ip:port
            return True
        elif ':' in proxy_string:
            # Format: ip:port or user:pass@ip:port
            parts = proxy_string.split(':')
            if len(parts) >= 2:
                return True
        return False
    
    def remove_proxy(self, proxy_string: str) -> bool:
        """Remove a proxy"""
        for i, proxy in enumerate(self.proxies):
            if proxy['proxy'] == proxy_string:
                self.proxies.pop(i)
                self.save_proxies()
                self.logger.info(f"Proxy removed: {proxy_string}")
                return True
        return False
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get a random active proxy"""
        active_proxies = [p for p in self.proxies if p['is_active']]
        if active_proxies:
            return random.choice(active_proxies)
        return None
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation"""
        active_proxies = [p for p in self.proxies if p['is_active']]
        if not active_proxies:
            return None
        
        proxy = active_proxies[self.current_proxy_index % len(active_proxies)]
        self.current_proxy_index += 1
        proxy['last_used'] = datetime.now().isoformat()
        self.save_proxies()
        
        return proxy
    
    def check_proxy(self, proxy_data: Dict) -> bool:
        """Check if proxy is working"""
        proxy_string = proxy_data['proxy']
        
        try:
            proxies = {
                'http': proxy_string,
                'https': proxy_string
            }
            
            test_url = "http://httpbin.org/ip"
            timeout = 10
            
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            
            if response.status_code == 200:
                proxy_data['last_checked'] = datetime.now().isoformat()
                proxy_data['is_active'] = True
                proxy_data['speed'] = int(response.elapsed.total_seconds() * 1000)
                self.logger.info(f"Proxy {proxy_string} is working (speed: {proxy_data['speed']}ms)")
                return True
                
        except Exception as e:
            self.logger.warning(f"Proxy {proxy_string} failed: {e}")
        
        proxy_data['is_active'] = False
        proxy_data['last_checked'] = datetime.now().isoformat()
        return False
    
    def check_all_proxies(self):
        """Check all proxies"""
        self.logger.info(f"Checking {len(self.proxies)} proxies...")
        
        working = 0
        for proxy in self.proxies:
            if self.check_proxy(proxy):
                working += 1
            time.sleep(1)  # Avoid rate limiting
        
        self.save_proxies()
        self.logger.info(f"Proxy check completed: {working}/{len(self.proxies)} working")
        
        return {
            'total': len(self.proxies),
            'working': working,
            'failed': len(self.proxies) - working
        }
    
    def get_proxy_formatted(self, proxy_data: Dict) -> Dict:
        """Get formatted proxy for requests library"""
        if not proxy_data:
            return {}
        
        proxy_string = proxy_data['proxy']
        proxy_type = proxy_data.get('type', 'http')
        
        return {
            'http': f"{proxy_type}://{proxy_string}",
            'https': f"{proxy_type}://{proxy_string}"
        }
    
    def import_proxies_from_file(self, file_path: str) -> int:
        """Import proxies from text file"""
        imported = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    proxy_string = line.strip()
                    if proxy_string:
                        if self.add_proxy(proxy_string):
                            imported += 1
            
            self.logger.info(f"Imported {imported} proxies from {file_path}")
            return imported
            
        except Exception as e:
            self.logger.error(f"Failed to import proxies: {e}")
            return 0
    
    def get_statistics(self) -> Dict:
        """Get proxy statistics"""
        total = len(self.proxies)
        active = len([p for p in self.proxies if p['is_active']])
        
        if active > 0:
            avg_speed = sum(p.get('speed', 0) for p in self.proxies if p['is_active']) / active
        else:
            avg_speed = 0
        
        countries = {}
        for proxy in self.proxies:
            country = proxy.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1
        
        return {
            'total_proxies': total,
            'active_proxies': active,
            'inactive_proxies': total - active,
            'avg_speed_ms': round(avg_speed, 2),
            'countries': countries
        }