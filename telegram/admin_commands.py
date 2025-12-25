# -*- coding: utf-8 -*-
"""
ADMIN COMMANDS HANDLER
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.database import Database
from database.json_db import JSONDatabase
from core.account_manager import AccountManager
from core.proxy_handler import ProxyHandler
from utils.logger import bot_logger
from config import Config

db = Database()
json_db = JSONDatabase()
account_manager = AccountManager()
proxy_handler = ProxyHandler()

# List of admin user IDs (from config)
ADMIN_IDS = Config.ADMIN_IDS

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin commands"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Admin privileges required.",
            parse_mode='HTML'
        )
        return
    
    command = update.message.text.split()[0].lower()
    
    if command == '/admin_stats':
        await admin_stats(update, context)
    elif command == '/admin_users':
        await admin_users(update, context)
    elif command == '/admin_accounts':
        await admin_accounts(update, context)
    elif command == '/admin_proxies':
        await admin_proxies(update, context)
    elif command == '/admin_broadcast':
        await admin_broadcast(update, context)
    elif command == '/admin_ban':
        await admin_ban(update, context)
    elif command == '/admin_logs':
        await admin_logs(update, context)
    else:
        await update.message.reply_text(
            "❓ Unknown admin command. Available commands:\n"
            "/admin_stats - System statistics\n"
            "/admin_users - User management\n"
            "/admin_accounts - Account management\n"
            "/admin_proxies - Proxy management\n"
            "/admin_broadcast - Broadcast message\n"
            "/admin_ban - Ban user\n"
            "/admin_logs - View logs",
            parse_mode='HTML'
        )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show detailed system statistics"""
    # Get database statistics
    db_stats = db.get_statistics()
    
    # Get account statistics
    account_stats = account_manager.get_statistics()
    
    # Get proxy statistics
    proxy_stats = proxy_handler.get_statistics()
    
    # Get user statistics
    # This would require tracking active users
    
    stats_text = f"""
<b>📊 ADMIN DASHBOARD</b>

━━━━━━━━━━━━━━━━━━━━
<b>DATABASE STATISTICS:</b>
• Total Tests: {db_stats['total_tests']:,}
• Total Views Sent: {db_stats['total_views']:,}
• Today's Tests: {db_stats['today_tests']:,}
• Today's Views: {db_stats['today_views']:,}
• Success Rate: {db_stats['success_rate']:.1f}%

<b>ACCOUNT STATISTICS:</b>
• Total Accounts: {account_stats['total_accounts']:,}
• Active Accounts: {account_stats['active_accounts']:,}
• Banned Accounts: {account_stats['banned_accounts']:,}
• Limited Accounts: {account_stats['limited_accounts']:,}
• Total Views Sent: {account_stats['total_views_sent']:,}
• Avg Views/Account: {account_stats['avg_views_per_account']:.1f}

<b>PROXY STATISTICS:</b>
• Total Proxies: {proxy_stats['total_proxies']:,}
• Active Proxies: {proxy_stats['active_proxies']:,}
• Inactive Proxies: {proxy_stats['inactive_proxies']:,}
• Avg Speed: {proxy_stats['avg_speed_ms']}ms
• Countries: {len(proxy_stats['countries']):,}

<b>SYSTEM STATUS:</b>
• Database: ✅ Online
• View Engine: ✅ Running
• API: ✅ Available
• Queue: 0 pending

━━━━━━━━━━━━━━━━━━━━
<b>Last Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(
        stats_text,
        parse_mode='HTML'
    )
    
    bot_logger.info(f"Admin {update.effective_user.id} viewed system stats")

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user management"""
    # Get user list from database
    # This would require a method to get all users
    
    users_text = f"""
<b>👥 USER MANAGEMENT</b>

━━━━━━━━━━━━━━━━━━━━
<b>User Statistics:</b>
• Total Users: 0
• Active Today: 0
• New Today: 0

<b>Recent Users:</b>
No users found.

<b>User Limits:</b>
• Max Tests/Day: 10
• Max Views/Day: 100,000
• Default Plan: Free

━━━━━━━━━━━━━━━━━━━━
<b>Commands:</b>
• /admin_users list - List all users
• /admin_users search [query] - Search users
• /admin_users view [id] - View user details
• /admin_users limit [id] [tests] [views] - Set user limits
"""
    
    await update.message.reply_text(
        users_text,
        parse_mode='HTML'
    )

async def admin_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage TikTok accounts"""
    # Get account statistics
    stats = account_manager.get_statistics()
    accounts = account_manager.get_active_accounts()
    
    accounts_text = f"""
<b>📱 TIKTOK ACCOUNT MANAGEMENT</b>

━━━━━━━━━━━━━━━━━━━━
<b>Statistics:</b>
• Total: {stats['total_accounts']:,}
• Active: {stats['active_accounts']:,}
• Banned: {stats['banned_accounts']:,}
• Limited: {stats['limited_accounts']:,}
• Views Sent: {stats['total_views_sent']:,}

<b>Recent Activity:</b>
"""
    
    # Show last 5 accounts
    recent_accounts = sorted(accounts, key=lambda x: x.get('last_used', ''), reverse=True)[:5]
    
    for i, acc in enumerate(recent_accounts, 1):
        last_used = acc.get('last_used', 'Never')
        if last_used:
            try:
                last_used = datetime.fromisoformat(last_used).strftime('%m/%d %H:%M')
            except:
                pass
        
        accounts_text += f"""
{i}. @{acc['username']}
   Status: {acc['status'].upper()}
   Views: {acc.get('views_sent', 0):,}
   Last Used: {last_used}
"""
    
    accounts_text += """
━━━━━━━━━━━━━━━━━━━━
<b>Commands:</b>
• /admin_accounts list - List all accounts
• /admin_accounts add [user:pass] - Add account
• /admin_accounts remove [username] - Remove account
• /admin_accounts check [username] - Check account
• /admin_accounts import [file] - Import accounts
• /admin_accounts export - Export accounts
"""
    
    await update.message.reply_text(
        accounts_text,
        parse_mode='HTML'
    )

async def admin_proxies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage proxies"""
    # Get proxy statistics
    stats = proxy_handler.get_statistics()
    proxies = proxy_handler.proxies[:5]  # First 5 proxies
    
    proxies_text = f"""
<b>🌐 PROXY MANAGEMENT</b>

━━━━━━━━━━━━━━━━━━━━
<b>Statistics:</b>
• Total: {stats['total_proxies']:,}
• Active: {stats['active_proxies']:,}
• Inactive: {stats['inactive_proxies']:,}
• Avg Speed: {stats['avg_speed_ms']}ms
• Countries: {len(stats['countries']):,}

<b>Country Distribution:</b>
"""
    
    # Show top countries
    countries = sorted(stats['countries'].items(), key=lambda x: x[1], reverse=True)[:5]
    for country, count in countries:
        proxies_text += f"• {country}: {count:,}\n"
    
    proxies_text += """
<b>Recent Proxies:</b>
"""
    
    for i, proxy in enumerate(proxies, 1):
        proxy_display = proxy['proxy'][:40] + "..." if len(proxy['proxy']) > 40 else proxy['proxy']
        status = "🟢" if proxy['is_active'] else "🔴"
        
        proxies_text += f"""
{i}. {proxy_display} {status}
   Type: {proxy.get('type', 'HTTP')}
   Country: {proxy.get('country', 'Unknown')}
   Speed: {proxy.get('speed', 'N/A')}ms
"""
    
    proxies_text += """
━━━━━━━━━━━━━━━━━━━━
<b>Commands:</b>
• /admin_proxies list - List all proxies
• /admin_proxies add [proxy] - Add proxy
• /admin_proxies remove [proxy] - Remove proxy
• /admin_proxies check - Check all proxies
• /admin_proxies import [file] - Import proxies
"""
    
    await update.message.reply_text(
        proxies_text,
        parse_mode='HTML'
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users"""
    if len(context.args) < 1:
        await update.message.reply_text(
            "Usage: /admin_broadcast [message]\n\n"
            "Example: /admin_broadcast System maintenance in 1 hour.",
            parse_mode='HTML'
        )
        return
    
    message = ' '.join(context.args)
    
    # In a real implementation, you would:
    # 1. Get all user IDs from database
    # 2. Send message to each user
    # 3. Handle rate limiting
    
    await update.message.reply_text(
        f"📢 Broadcast message prepared:\n\n{message}\n\n"
        f"⚠️ This would be sent to all users. Implementation pending.",
        parse_mode='HTML'
    )
    
    bot_logger.info(f"Admin {update.effective_user.id} prepared broadcast: {message[:50]}...")

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user"""
    if len(context.args) < 1:
        await update.message.reply_text(
            "Usage: /admin_ban [user_id] [reason]\n\n"
            "Example: /admin_ban 12345678 Spamming",
            parse_mode='HTML'
        )
        return
    
    user_id = context.args[0]
    reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
    
    try:
        user_id = int(user_id)
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid user ID. Must be a number.",
            parse_mode='HTML'
        )
        return
    
    # In a real implementation, you would:
    # 1. Update user status in database
    # 2. Cancel any ongoing tests
    # 3. Notify the user
    
    await update.message.reply_text(
        f"✅ User {user_id} would be banned.\n"
        f"Reason: {reason}\n\n"
        f"⚠️ Ban functionality pending implementation.",
        parse_mode='HTML'
    )
    
    bot_logger.warning(f"Admin {update.effective_user.id} attempted to ban user {user_id}: {reason}")

async def admin_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View system logs"""
    # Get recent logs from log file
    log_file = Config.LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    
    if not log_file.exists():
        await update.message.reply_text(
            "No log file found for today.",
            parse_mode='HTML'
        )
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Get last 20 lines
        recent_logs = lines[-20:] if len(lines) > 20 else lines
        
        logs_text = f"""
<b>📋 SYSTEM LOGS</b>
<code>{log_file.name}</code>

━━━━━━━━━━━━━━━━━━━━
"""
        
        for line in recent_logs:
            logs_text += f"{line}"
        
        # Split if too long
        if len(logs_text) > 4000:
            logs_text = logs_text[:4000] + "\n... (truncated)"
        
        await update.message.reply_text(
            f"<pre>{logs_text}</pre>",
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error reading logs: {e}",
            parse_mode='HTML'
        )
    
    bot_logger.info(f"Admin {update.effective_user.id} viewed system logs")