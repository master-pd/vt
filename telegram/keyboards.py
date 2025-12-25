# -*- coding: utf-8 -*-
"""
INLINE KEYBOARDS FOR TELEGRAM BOT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    """Get main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Start Test", callback_data="start_test"),
            InlineKeyboardButton("📈 Statistics", callback_data="stats")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_view_count_keyboard():
    """Get view count selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("100 Views", callback_data="views_100"),
            InlineKeyboardButton("500 Views", callback_data="views_500"),
            InlineKeyboardButton("1,000 Views", callback_data="views_1000")
        ],
        [
            InlineKeyboardButton("2,500 Views", callback_data="views_2500"),
            InlineKeyboardButton("5,000 Views", callback_data="views_5000"),
            InlineKeyboardButton("10,000 Views", callback_data="views_10000")
        ],
        [
            InlineKeyboardButton("Custom Amount", callback_data="custom_views"),
            InlineKeyboardButton("⬅️ Back", callback_data="back")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_custom_view_keyboard():
    """Get custom view input keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("100", callback_data="custom_100"),
            InlineKeyboardButton("500", callback_data="custom_500"),
            InlineKeyboardButton("1,000", callback_data="custom_1000")
        ],
        [
            InlineKeyboardButton("2,000", callback_data="custom_2000"),
            InlineKeyboardButton("5,000", callback_data="custom_5000"),
            InlineKeyboardButton("10,000", callback_data="custom_10000")
        ],
        [
            InlineKeyboardButton("Enter Manually", callback_data="manual_input"),
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_test_confirmation_keyboard():
    """Get test confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Start Test", callback_data="confirm_start"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel_test")
        ],
        [
            InlineKeyboardButton("⚙️ Change Settings", callback_data="change_settings")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    """Get settings keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔧 Account Settings", callback_data="account_settings"),
            InlineKeyboardButton("🌐 Proxy Settings", callback_data="proxy_settings")
        ],
        [
            InlineKeyboardButton("⚡ Speed Settings", callback_data="speed_settings"),
            InlineKeyboardButton("📊 View Settings", callback_data="view_settings")
        ],
        [
            InlineKeyboardButton("💾 Save Settings", callback_data="save_settings"),
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_speed_settings_keyboard():
    """Get speed settings keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🐢 Slow (100/min)", callback_data="speed_100"),
            InlineKeyboardButton("🚶 Normal (1,000/min)", callback_data="speed_1000")
        ],
        [
            InlineKeyboardButton("🚗 Fast (5,000/min)", callback_data="speed_5000"),
            InlineKeyboardButton("🚀 Turbo (10,000/min)", callback_data="speed_10000")
        ],
        [
            InlineKeyboardButton("📊 Custom Speed", callback_data="custom_speed"),
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_settings")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_account_management_keyboard():
    """Get account management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("➕ Add Account", callback_data="add_account"),
            InlineKeyboardButton("➖ Remove Account", callback_data="remove_account")
        ],
        [
            InlineKeyboardButton("📋 List Accounts", callback_data="list_accounts"),
            InlineKeyboardButton("🔄 Check Status", callback_data="check_accounts")
        ],
        [
            InlineKeyboardButton("📥 Import", callback_data="import_accounts"),
            InlineKeyboardButton("📤 Export", callback_data="export_accounts")
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_settings")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_proxy_management_keyboard():
    """Get proxy management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("➕ Add Proxy", callback_data="add_proxy"),
            InlineKeyboardButton("➖ Remove Proxy", callback_data="remove_proxy")
        ],
        [
            InlineKeyboardButton("📋 List Proxies", callback_data="list_proxies"),
            InlineKeyboardButton("✅ Check Proxies", callback_data="check_proxies")
        ],
        [
            InlineKeyboardButton("📥 Import Proxies", callback_data="import_proxies"),
            InlineKeyboardButton("⚙️ Proxy Settings", callback_data="proxy_config")
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_settings")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_test_status_keyboard(test_id: str):
    """Get test status keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{test_id}"),
            InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{test_id}")
        ],
        [
            InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{test_id}"),
            InlineKeyboardButton("📊 Details", callback_data=f"details_{test_id}")
        ],
        [
            InlineKeyboardButton("📋 Report", callback_data=f"report_{test_id}"),
            InlineKeyboardButton("⬅️ Back", callback_data="back_to_tests")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Get admin keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📊 System Stats", callback_data="admin_stats"),
            InlineKeyboardButton("👥 User Management", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("💰 Payment Stats", callback_data="admin_payments"),
            InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban")
        ],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
            InlineKeyboardButton("⚙️ System Settings", callback_data="admin_settings")
        ],
        [
            InlineKeyboardButton("⬅️ Main Menu", callback_data="back_to_main")
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

def get_pagination_keyboard(page: int, total_pages: int, prefix: str):
    """Get pagination keyboard"""
    keyboard = []
    
    # Page numbers
    row = []
    if page > 1:
        row.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"{prefix}_page_{page-1}"))
    
    row.append(InlineKeyboardButton(f"Page {page}/{total_pages}", callback_data="current_page"))
    
    if page < total_pages:
        row.append(InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}_page_{page+1}"))
    
    keyboard.append(row)
    
    # Navigation
    keyboard.append([
        InlineKeyboardButton("⬅️ Back", callback_data=f"back_from_{prefix}"),
        InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")
    ])
    
    return InlineKeyboardMarkup(keyboard)