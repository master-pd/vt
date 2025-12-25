# -*- coding: utf-8 -*-
"""
TELEGRAM MODULE INITIALIZATION
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

from .bot_core import TelegramBot
from .handlers import (
    handle_start,
    handle_help_command,
    handle_stats_command,
    handle_video_url,
    handle_view_selection,
    handle_cancel,
    handle_admin_stats
)
from .keyboards import (
    get_main_menu,
    get_view_count_keyboard,
    get_test_confirmation_keyboard,
    get_settings_keyboard,
    get_admin_keyboard
)
from .message_templates import (
    get_welcome_message,
    get_test_started_message,
    get_test_progress_message,
    get_test_completed_message,
    get_system_stats_message
)
from .user_manager import UserManager
from .admin_commands import (
    handle_admin_command,
    admin_stats,
    admin_users,
    admin_accounts,
    admin_proxies,
    admin_broadcast,
    admin_ban,
    admin_logs
)
from .payment_handler import PaymentHandler

__all__ = [
    # Bot core
    'TelegramBot',
    
    # Handlers
    'handle_start',
    'handle_help_command',
    'handle_stats_command',
    'handle_video_url',
    'handle_view_selection',
    'handle_cancel',
    'handle_admin_stats',
    
    # Keyboards
    'get_main_menu',
    'get_view_count_keyboard',
    'get_test_confirmation_keyboard',
    'get_settings_keyboard',
    'get_admin_keyboard',
    
    # Message templates
    'get_welcome_message',
    'get_test_started_message',
    'get_test_progress_message',
    'get_test_completed_message',
    'get_system_stats_message',
    
    # User management
    'UserManager',
    
    # Admin commands
    'handle_admin_command',
    'admin_stats',
    'admin_users',
    'admin_accounts',
    'admin_proxies',
    'admin_broadcast',
    'admin_ban',
    'admin_logs',
    
    # Payment handler
    'PaymentHandler'
]