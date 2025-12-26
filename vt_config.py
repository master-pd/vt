"""
VT BOT CONFIGURATION - DYNAMIC SETTINGS
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

class VTConfig:
    """Dynamic configuration manager for VT Bot"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.base_dir = Path(__file__).parent
            self.data_dir = self.base_dir / 'data'
            self.config_dir = self.data_dir / 'config'
            
            # Default configuration
            self.default_config = self._get_default_config()
            
            # Runtime configuration
            self.config = {}
            self.runtime_config = {}
            
            # Load configurations
            self.load_configurations()
            self.initialized = True
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "system": {
                "name": "VT Bot Ultra Pro",
                "version": "4.0.0",
                "author": "MASTER (RANA)",
                "team": "MAR PD",
                "environment": "production",
                "debug": False,
                "log_level": "INFO"
            },
            "performance": {
                "max_concurrent_tasks": 50,
                "max_views_per_minute": 10000,
                "request_timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 5,
                "batch_size": 100,
                "queue_size": 1000
            },
            "tiktok": {
                "base_url": "https://www.tiktok.com",
                "api_url": "https://api.tiktok.com",
                "video_patterns": [
                    r"https?://(www\.|vm\.|vt\.)?tiktok\.com/@[\w.-]+/video/\d+",
                    r"https?://(www\.)?tiktok\.com/t/[\w-]+",
                    r"https?://(www\.)?tiktok\.com/[\w-]+"
                ],
                "min_views": 1,
                "max_views": 100000,
                "default_views": 1000
            },
            "security": {
                "protect_local_ip": True,
                "use_proxy_rotation": True,
                "proxy_timeout": 10,
                "session_rotation": True,
                "session_lifetime": 3600,
                "cookie_rotation": True,
                "user_agent_rotation": True
            },
            "anti_detection": {
                "random_delays": True,
                "min_delay": 1,
                "max_delay": 5,
                "human_like_behavior": True,
                "mouse_movements": True,
                "scroll_randomization": True,
                "time_spent_variance": True,
                "referrer_spoofing": True
            },
            "proxy": {
                "types": ["http", "https", "socks4", "socks5"],
                "test_url": "https://www.tiktok.com",
                "test_timeout": 10,
                "max_proxies": 1000,
                "rotation_interval": 100,
                "speed_threshold": 5000
            },
            "accounts": {
                "max_accounts": 1000,
                "auto_cleanup": True,
                "health_check_interval": 3600,
                "usage_limit": 100,
                "cooldown_period": 3600
            },
            "paths": {
                "accounts_file": "data/accounts/active_accounts.json",
                "proxies_file": "data/proxies/proxy_list.json",
                "sessions_dir": "data/sessions",
                "logs_dir": "data/logs",
                "cache_dir": "data/cache",
                "config_file": "data/config/settings.json"
            },
            "ui": {
                "colors_enabled": True,
                "animation_enabled": True,
                "progress_bars": True,
                "real_time_stats": True,
                "auto_refresh": True,
                "theme": "dark"
            },
            "logging": {
                "enabled": True,
                "level": "INFO",
                "file_logging": True,
                "console_logging": True,
                "max_log_size": 10485760,  # 10MB
                "backup_count": 5,
                "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def load_configurations(self):
        """Load all configurations"""
        try:
            # Load from file if exists
            config_file = self.config_dir / "settings.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config.copy()
                self.save_config()
            
            # Load runtime config
            runtime_file = self.config_dir / "runtime_config.json"
            if runtime_file.exists():
                with open(runtime_file, 'r', encoding='utf-8') as f:
                    self.runtime_config = json.load(f)
            
            # Ensure directories exist
            self._ensure_directories()
            
        except Exception as e:
            print(f"Config load error: {e}")
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            config_file = self.config_dir / "settings.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Config save error: {e}")
    
    def save_runtime_config(self):
        """Save runtime configuration"""
        try:
            runtime_file = self.config_dir / "runtime_config.json"
            with open(runtime_file, 'w', encoding='utf-8') as f:
                json.dump(self.runtime_config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Runtime config save error: {e}")
    
    def _ensure_directories(self):
        """Ensure all directories exist"""
        paths = self.get("paths", {})
        for key, path in paths.items():
            if key.endswith("_dir"):
                dir_path = self.base_dir / path
                dir_path.mkdir(parents=True, exist_ok=True)
            elif key.endswith("_file"):
                file_path = self.base_dir / path
                file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        for key, value in updates.items():
            self.set(key, value)
    
    def get_runtime(self, key: str, default: Any = None) -> Any:
        """Get runtime configuration value"""
        return self.runtime_config.get(key, default)
    
    def set_runtime(self, key: str, value: Any):
        """Set runtime configuration value"""
        self.runtime_config[key] = value
        self.save_runtime_config()
    
    def reset_to_default(self):
        """Reset to default configuration"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance settings"""
        return self.get("performance", {})
    
    def get_tiktok_settings(self) -> Dict[str, Any]:
        """Get TikTok settings"""
        return self.get("tiktok", {})
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security settings"""
        return self.get("security", {})
    
    def get_anti_detection_settings(self) -> Dict[str, Any]:
        """Get anti-detection settings"""
        return self.get("anti_detection", {})
    
    def get_path(self, key: str) -> Path:
        """Get path from configuration"""
        path_str = self.get(f"paths.{key}")
        if path_str:
            return self.base_dir / path_str
        return None
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get("system.debug", False)
    
    def get_log_level(self) -> str:
        """Get log level"""
        return self.get("logging.level", "INFO")
    
    def get_max_concurrent(self) -> int:
        """Get max concurrent tasks"""
        return self.get("performance.max_concurrent_tasks", 50)
    
    def get_max_views_per_minute(self) -> int:
        """Get max views per minute"""
        return self.get("performance.max_views_per_minute", 10000)
    
    def get_request_timeout(self) -> int:
        """Get request timeout"""
        return self.get("performance.request_timeout", 30)
    
    def get_retry_attempts(self) -> int:
        """Get retry attempts"""
        return self.get("performance.retry_attempts", 3)
    
    def get_retry_delay(self) -> int:
        """Get retry delay"""
        return self.get("performance.retry_delay", 5)
    
    def get_video_patterns(self) -> List[str]:
        """Get TikTok video URL patterns"""
        return self.get("tiktok.video_patterns", [])
    
    def get_min_views(self) -> int:
        """Get minimum views"""
        return self.get("tiktok.min_views", 1)
    
    def get_max_views(self) -> int:
        """Get maximum views"""
        return self.get("tiktok.max_views", 100000)
    
    def get_default_views(self) -> int:
        """Get default views"""
        return self.get("tiktok.default_views", 1000)
    
    def should_protect_local_ip(self) -> bool:
        """Check if local IP should be protected"""
        return self.get("security.protect_local_ip", True)
    
    def should_use_proxy_rotation(self) -> bool:
        """Check if proxy rotation should be used"""
        return self.get("security.use_proxy_rotation", True)
    
    def should_rotate_sessions(self) -> bool:
        """Check if sessions should be rotated"""
        return self.get("security.session_rotation", True)
    
    def get_session_lifetime(self) -> int:
        """Get session lifetime in seconds"""
        return self.get("security.session_lifetime", 3600)
    
    def should_use_random_delays(self) -> bool:
        """Check if random delays should be used"""
        return self.get("anti_detection.random_delays", True)
    
    def get_min_delay(self) -> int:
        """Get minimum delay in seconds"""
        return self.get("anti_detection.min_delay", 1)
    
    def get_max_delay(self) -> int:
        """Get maximum delay in seconds"""
        return self.get("anti_detection.max_delay", 5)
    
    def should_simulate_human_behavior(self) -> bool:
        """Check if human behavior should be simulated"""
        return self.get("anti_detection.human_like_behavior", True)
    
    def get_proxy_types(self) -> List[str]:
        """Get proxy types"""
        return self.get("proxy.types", ["http", "https", "socks4", "socks5"])
    
    def get_proxy_test_url(self) -> str:
        """Get proxy test URL"""
        return self.get("proxy.test_url", "https://www.tiktok.com")
    
    def get_proxy_test_timeout(self) -> int:
        """Get proxy test timeout"""
        return self.get("proxy.test_timeout", 10)
    
    def get_max_proxies(self) -> int:
        """Get maximum proxies"""
        return self.get("proxy.max_proxies", 1000)
    
    def get_rotation_interval(self) -> int:
        """Get rotation interval"""
        return self.get("proxy.rotation_interval", 100)
    
    def get_speed_threshold(self) -> int:
        """Get speed threshold"""
        return self.get("proxy.speed_threshold", 5000)
    
    def get_max_accounts(self) -> int:
        """Get maximum accounts"""
        return self.get("accounts.max_accounts", 1000)
    
    def should_auto_cleanup_accounts(self) -> bool:
        """Check if accounts should be auto-cleaned"""
        return self.get("accounts.auto_cleanup", True)
    
    def get_account_health_check_interval(self) -> int:
        """Get account health check interval"""
        return self.get("accounts.health_check_interval", 3600)
    
    def get_account_usage_limit(self) -> int:
        """Get account usage limit"""
        return self.get("accounts.usage_limit", 100)
    
    def get_account_cooldown_period(self) -> int:
        """Get account cooldown period"""
        return self.get("accounts.cooldown_period", 3600)
    
    def are_colors_enabled(self) -> bool:
        """Check if colors are enabled"""
        return self.get("ui.colors_enabled", True)
    
    def is_animation_enabled(self) -> bool:
        """Check if animation is enabled"""
        return self.get("ui.animation_enabled", True)
    
    def are_progress_bars_enabled(self) -> bool:
        """Check if progress bars are enabled"""
        return self.get("ui.progress_bars", True)
    
    def is_logging_enabled(self) -> bool:
        """Check if logging is enabled"""
        return self.get("logging.enabled", True)
    
    def is_file_logging_enabled(self) -> bool:
        """Check if file logging is enabled"""
        return self.get("logging.file_logging", True)
    
    def is_console_logging_enabled(self) -> bool:
        """Check if console logging is enabled"""
        return self.get("logging.console_logging", True)
    
    def get_max_log_size(self) -> int:
        """Get maximum log size"""
        return self.get("logging.max_log_size", 10485760)
    
    def get_log_backup_count(self) -> int:
        """Get log backup count"""
        return self.get("logging.backup_count", 5)
    
    def get_log_format(self) -> str:
        """Get log format"""
        return self.get("logging.log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Global configuration instance
config = VTConfig()

def get_config() -> VTConfig:
    """Get global configuration instance"""
    return config