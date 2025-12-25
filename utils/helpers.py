# -*- coding: utf-8 -*-
"""
HELPER FUNCTIONS - GENERAL UTILITY FUNCTIONS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import os
import sys
import json
import random
import string
import hashlib
import time
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

class Helpers:
    @staticmethod
    def generate_id(prefix: str = '', length: int = 8) -> str:
        """Generate unique ID"""
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choices(chars, k=length))
        
        if prefix:
            return f"{prefix}-{random_part}"
        return random_part
    
    @staticmethod
    def generate_test_id() -> str:
        """Generate test ID"""
        timestamp = int(time.time())
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"VT{timestamp}{random_part}"
    
    @staticmethod
    def calculate_hash(data: Union[str, bytes]) -> str:
        """Calculate SHA256 hash"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def format_number(number: int) -> str:
        """Format number with commas"""
        return f"{number:,}"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f}h"
        else:
            days = seconds / 86400
            return f"{days:.1f}d"
    
    @staticmethod
    def format_bytes(size: int) -> str:
        """Format bytes in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    @staticmethod
    def parse_duration(duration_str: str) -> int:
        """Parse duration string to seconds"""
        duration_str = duration_str.strip().lower()
        
        if duration_str.endswith('s'):
            return int(duration_str[:-1])
        elif duration_str.endswith('m'):
            return int(duration_str[:-1]) * 60
        elif duration_str.endswith('h'):
            return int(duration_str[:-1]) * 3600
        elif duration_str.endswith('d'):
            return int(duration_str[:-1]) * 86400
        else:
            try:
                return int(duration_str)
            except:
                return 0
    
    @staticmethod
    def get_timestamp(format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """Get current timestamp"""
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def get_date_range(days: int = 7) -> List[str]:
        """Get list of dates for range"""
        dates = []
        today = datetime.now()
        
        for i in range(days):
            date = today - timedelta(days=i)
            dates.append(date.strftime('%Y-%m-%d'))
        
        return dates
    
    @staticmethod
    def chunk_list(lst: List, chunk_size: int) -> List[List]:
        """Split list into chunks"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def flatten_list(nested_list: List) -> List:
        """Flatten nested list"""
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(Helpers.flatten_list(item))
            else:
                flat_list.append(item)
        return flat_list
    
    @staticmethod
    def safe_get(dictionary: Dict, keys: List, default: Any = None) -> Any:
        """Safely get value from nested dictionary"""
        current = dictionary
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    @staticmethod
    def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
        """Merge two dictionaries"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Helpers.merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result
    
    @staticmethod
    def filter_dict(dictionary: Dict, keys: List) -> Dict:
        """Filter dictionary to include only specified keys"""
        return {k: dictionary[k] for k in keys if k in dictionary}
    
    @staticmethod
    def sort_dict_by_value(dictionary: Dict, reverse: bool = False) -> Dict:
        """Sort dictionary by value"""
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=reverse)}
    
    @staticmethod
    def calculate_percentage(part: int, whole: int) -> float:
        """Calculate percentage"""
        if whole == 0:
            return 0.0
        return (part / whole) * 100
    
    @staticmethod
    def calculate_average(numbers: List[float]) -> float:
        """Calculate average"""
        if not numbers:
            return 0.0
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def calculate_median(numbers: List[float]) -> float:
        """Calculate median"""
        if not numbers:
            return 0.0
        
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        
        if n % 2 == 0:
            mid1 = sorted_numbers[n // 2 - 1]
            mid2 = sorted_numbers[n // 2]
            return (mid1 + mid2) / 2
        else:
            return sorted_numbers[n // 2]
    
    @staticmethod
    def calculate_percentile(numbers: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not numbers:
            return 0.0
        
        sorted_numbers = sorted(numbers)
        index = (percentile / 100) * (len(sorted_numbers) - 1)
        
        if index.is_integer():
            return sorted_numbers[int(index)]
        else:
            lower = sorted_numbers[int(index)]
            upper = sorted_numbers[int(index) + 1]
            return lower + (upper - lower) * (index % 1)
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Generate random string"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_random_number(min_val: int = 1000, max_val: int = 9999) -> int:
        """Generate random number"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except:
            return False
    
    @staticmethod
    def read_file(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
        """Read file content"""
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except:
            return None
    
    @staticmethod
    def write_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
        """Write content to file"""
        try:
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except:
            return False
    
    @staticmethod
    def append_file(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
        """Append content to file"""
        try:
            with open(filepath, 'a', encoding=encoding) as f:
                f.write(content)
            return True
        except:
            return False
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete file"""
        try:
            os.remove(filepath)
            return True
        except:
            return False
    
    @staticmethod
    def list_files(directory: str, pattern: str = '*') -> List[str]:
        """List files in directory"""
        try:
            import glob
            return glob.glob(os.path.join(directory, pattern))
        except:
            return []
    
    @staticmethod
    def execute_command(command: str) -> tuple:
        """Execute shell command"""
        try:
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, '', str(e)
    
    @staticmethod
    async def async_sleep(seconds: float):
        """Async sleep"""
        await asyncio.sleep(seconds)
    
    @staticmethod
    def retry_operation(operation, max_attempts: int = 3, delay: float = 1.0):
        """Retry operation with exponential backoff"""
        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                
                sleep_time = delay * (2 ** attempt)
                time.sleep(sleep_time)
        
        return None
    
    @staticmethod
    def create_progress_bar(progress: float, width: int = 20) -> str:
        """Create progress bar string"""
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List], padding: int = 2) -> str:
        """Format data as table"""
        if not headers or not rows:
            return ""
        
        # Calculate column widths
        col_widths = [len(str(h)) + padding for h in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                cell_len = len(str(cell)) + padding
                if cell_len > col_widths[i]:
                    col_widths[i] = cell_len
        
        # Build table
        table = []
        
        # Header
        header_row = "│".join([str(h).ljust(col_widths[i]) for i, h in enumerate(headers)])
        table.append(header_row)
        
        # Separator
        separator = "─" * (sum(col_widths) + len(headers) - 1)
        table.append(separator)
        
        # Rows
        for row in rows:
            row_str = "│".join([str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)])
            table.append(row_str)
        
        return "\n".join(table)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number"""
        import re
        # Basic phone validation
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename"""
        import re
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Limit length
        filename = filename[:255]
        return filename
    
    @staticmethod
    def get_system_info() -> Dict:
        """Get system information"""
        import platform
        import psutil
        
        info = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_total': psutil.disk_usage('/').total,
            'disk_free': psutil.disk_usage('/').free
        }
        
        return info
    
    @staticmethod
    def get_memory_usage() -> Dict:
        """Get memory usage information"""
        import psutil
        process = psutil.Process()
        
        return {
            'rss': process.memory_info().rss,  # Resident Set Size
            'vms': process.memory_info().vms,  # Virtual Memory Size
            'percent': process.memory_percent(),
            'available': psutil.virtual_memory().available,
            'total': psutil.virtual_memory().total
        }