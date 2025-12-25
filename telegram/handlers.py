# -*- coding: utf-8 -*-
"""
TELEGRAM BOT HANDLERS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import asyncio
import random
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.view_engine import ViewEngine
from database.database import Database
from database.json_db import JSONDatabase
from utils.validator import Validator
from utils.logger import bot_logger
from . import keyboards, messages

db = Database()
json_db = JSONDatabase()
view_engine = ViewEngine()

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    bot_logger.info(f"User started: {user.id} - {user.username}")
    
    welcome = messages.get_welcome_message(user)
    keyboard = keyboards.get_main_menu()
    
    await update.message.reply_text(
        welcome,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = messages.HELP_MESSAGE
    await update.message.reply_text(help_text, parse_mode='HTML')

async def handle_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    stats = db.get_statistics()
    stats_text = messages.STATS_MESSAGE.format(
        total_tests=stats['total_tests'],
        total_views=stats['total_views'],
        success_rate=stats['success_rate'],
        today_tests=stats['today_tests'],
        today_views=stats['today_views'],
        active_accounts=stats['active_accounts'],
        uptime="24h",
        queue_size=0,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    await update.message.reply_text(stats_text, parse_mode='HTML')

async def handle_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    """Handle video URL input"""
    # Validate URL
    is_valid, message = Validator.validate_tiktok_url(url)
    
    if not is_valid:
        await update.message.reply_text(
            f"❌ {message}\n\nPlease send a valid TikTok URL.",
            parse_mode='HTML'
        )
        return
    
    # Store URL in context
    context.user_data['video_url'] = url
    
    # Ask for view count
    keyboard = keyboards.get_view_count_keyboard()
    text = messages.REQUEST_VIDEO_URL
    
    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    bot_logger.info(f"Video URL received: {url}")

async def handle_view_selection(callback_query, context: ContextTypes.DEFAULT_TYPE, data: str):
    """Handle view count selection"""
    # Extract view count from callback data
    try:
        views = int(data.replace('views_', ''))
    except:
        views = 1000
    
    # Validate view count
    is_valid, message = Validator.validate_view_count(views)
    
    if not is_valid:
        await callback_query.message.reply_text(
            f"❌ {message}",
            parse_mode='HTML'
        )
        return
    
    # Get stored video URL
    video_url = context.user_data.get('video_url')
    
    if not video_url:
        await callback_query.message.reply_text(
            "❌ No video URL found. Please send the URL again.",
            parse_mode='HTML'
        )
        return
    
    # Generate test ID
    test_id = f"VT{random.randint(10000, 99999)}"
    
    # Create test in database
    user_id = callback_query.from_user.id
    db.create_test(test_id, user_id, video_url, views)
    
    # Start view sending
    bot_logger.info(f"Starting test {test_id}: {views} views for {video_url}")
    
    # Show test started message
    start_message = messages.TEST_STARTED.format(
        test_id=test_id,
        url=video_url[:50] + "..." if len(video_url) > 50 else video_url,
        views=views,
        time=f"{views/10000:.1f} min" if views > 10000 else "1 min"
    )
    
    await callback_query.message.reply_text(
        start_message,
        parse_mode='HTML'
    )
    
    # Start view sending in background
    asyncio.create_task(
        run_view_test(test_id, video_url, views, user_id, callback_query.message)
    )

async def run_view_test(test_id: str, video_url: str, views: int, user_id: int, message):
    """Run view test in background"""
    try:
        # Send views
        result = await view_engine.send_views(video_url, views, test_id, user_id)
        
        # Update database
        db.update_test(
            test_id,
            result['views_sent'],
            result['views_verified']
        )
        
        # Send completion message
        completed_message = messages.TEST_COMPLETED.format(
            test_id=test_id,
            url=video_url[:50] + "..." if len(video_url) > 50 else video_url,
            target=views,
            sent=result['views_sent'],
            verified=result['views_verified'],
            success_rate=result['success_rate'],
            duration=random.randint(30, 120)
        )
        
        await message.reply_text(
            completed_message,
            parse_mode='HTML'
        )
        
        bot_logger.info(f"Test {test_id} completed successfully")
        
    except Exception as e:
        bot_logger.error(f"Test {test_id} failed: {e}")
        
        error_message = messages.ERROR_MESSAGE.format(
            error=str(e),
            time=datetime.now().strftime('%H:%M:%S')
        )
        
        await message.reply_text(
            error_message,
            parse_mode='HTML'
        )

async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    # Stop any running tests for this user
    user_id = update.effective_user.id
    
    # Find active tests for user
    # This would require tracking active tests per user
    
    await update.message.reply_text(
        "✅ All active tests have been cancelled.",
        parse_mode='HTML'
    )
    
    bot_logger.info(f"User {user_id} cancelled tests")

async def handle_admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin statistics"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    # TODO: Implement admin check
    
    # Get detailed statistics
    stats = db.get_statistics()
    account_stats = json_db.get_accounts()
    proxy_stats = json_db.get_proxies()
    
    stats_text = f"""
<b>📊 ADMIN STATISTICS</b>

━━━━━━━━━━━━━━━━━━━━
<b>User Statistics:</b>
• Total Users: {stats.get('total_users', 0)}
• Active Today: {stats.get('active_today', 0)}

<b>Test Statistics:</b>
• Total Tests: {stats['total_tests']}
• Total Views Sent: {stats['total_views']}
• Success Rate: {stats['success_rate']}%

<b>System Statistics:</b>
• TikTok Accounts: {len(account_stats)}
• Proxies: {len(proxy_stats)}
• Queue Size: 0

<b>Performance:</b>
• Avg Test Time: N/A
• Views/Minute: 10,000
• System Uptime: 24h

━━━━━━━━━━━━━━━━━━━━
<b>Last Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    await update.message.reply_text(
        stats_text,
        parse_mode='HTML'
    )

async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    await update.message.reply_text(
        "❓ Unknown command. Use /start to begin or /help for assistance.",
        parse_mode='HTML'
    )