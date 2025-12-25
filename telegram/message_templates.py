# -*- coding: utf-8 -*-
"""
MESSAGE TEMPLATES FOR TELEGRAM BOT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

from datetime import datetime

def get_welcome_message(user):
    """Generate welcome message"""
    return f"""
<b>🚀 TIKTOK VIEW TESTER</b>
<code>Professional Testing Platform</code>

━━━━━━━━━━━━━━━━━━━━
<b>Welcome, {user.first_name}!</b>

I am an advanced TikTok automation system designed for professional testing and analysis.

━━━━━━━━━━━━━━━━━━━━
<b>📋 HOW TO USE:</b>
1. Send me a TikTok video URL
2. Select desired view count
3. System processes your request
4. Receive detailed analytics

<b>⚡ FEATURES:</b>
• 10-10,000 views per minute
• Real-time progress tracking
• Detailed success analytics
• 24/7 automated service

━━━━━━━━━━━━━━━━━━━━
<b>📩 Send me a TikTok video URL to begin.</b>
"""

def get_test_started_message(test_id, video_url, views):
    """Generate test started message"""
    estimated_time = calculate_estimated_time(views)
    
    return f"""
<b>✅ TEST STARTED</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test ID:</b> <code>{test_id}</code>
<b>Video URL:</b> {shorten_url(video_url)}
<b>Target Views:</b> {views:,}
<b>Estimated Time:</b> {estimated_time}
<b>Start Time:</b> {datetime.now().strftime('%H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>INITIALIZING...</code>
<b>Progress:</b> 0%
<b>Views Sent:</b> 0/{views:,}
"""

def get_test_progress_message(test_id, current, total, speed, success_rate):
    """Generate test progress message"""
    percentage = (current / total) * 100
    progress_bar = generate_progress_bar(percentage)
    estimated_remaining = calculate_remaining_time(current, total, speed)
    
    return f"""
<b>📊 TEST IN PROGRESS</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test ID:</b> <code>{test_id}</code>
<b>Progress:</b> {progress_bar} {percentage:.1f}%
<b>Views Sent:</b> {current:,}/{total:,}
<b>Speed:</b> {speed:,}/minute
<b>Success Rate:</b> {success_rate:.1f}%
<b>ETA:</b> {estimated_remaining}

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>RUNNING</code>
<b>Last Update:</b> {datetime.now().strftime('%H:%M:%S')}
"""

def get_test_completed_message(test_id, video_url, target, sent, verified, success_rate, duration):
    """Generate test completed message"""
    return f"""
<b>🏁 TEST COMPLETED</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test ID:</b> <code>{test_id}</code>
<b>Video URL:</b> {shorten_url(video_url)}
<b>Target Views:</b> {target:,}
<b>Views Sent:</b> {sent:,}
<b>Views Verified:</b> {verified:,}
<b>Success Rate:</b> {success_rate:.1f}%
<b>Duration:</b> {duration:.1f} seconds

━━━━━━━━━━━━━━━━━━━━
<b>STATISTICS:</b>
• Delivery Rate: {(sent/target*100):.1f}%
• Verification Rate: {(verified/sent*100):.1f}%
• Views/Minute: {(sent/(duration/60)):.0f}
• Efficiency Score: {calculate_efficiency_score(success_rate, duration):.1f}/10

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>COMPLETED</code>
<b>Finish Time:</b> {datetime.now().strftime('%H:%M:%S')}
"""

def get_account_list_message(accounts, page, total_pages):
    """Generate account list message"""
    message = f"""
<b>📋 TIKTOK ACCOUNTS</b>
<code>Page {page}/{total_pages}</code>

━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, acc in enumerate(accounts, 1):
        status_emoji = "🟢" if acc['status'] == 'active' else "🔴" if acc['status'] == 'banned' else "🟡"
        message += f"""
<b>{i}. @{acc['username']}</b> {status_emoji}
• Status: {acc['status'].upper()}
• Views Sent: {acc.get('views_sent', 0):,}
• Last Used: {format_date(acc.get('last_used'))}
"""
    
    message += "\n━━━━━━━━━━━━━━━━━━━━"
    return message

def get_proxy_list_message(proxies, page, total_pages):
    """Generate proxy list message"""
    message = f"""
<b>🌐 PROXY LIST</b>
<code>Page {page}/{total_pages}</code>

━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, proxy in enumerate(proxies, 1):
        status_emoji = "🟢" if proxy['is_active'] else "🔴"
        speed = proxy.get('speed', 0)
        speed_text = f"{speed}ms" if speed else "N/A"
        
        message += f"""
<b>{i}. {shorten_proxy(proxy['proxy'])}</b> {status_emoji}
• Type: {proxy.get('type', 'HTTP')}
• Country: {proxy.get('country', 'Unknown')}
• Speed: {speed_text}
• Status: {'Active' if proxy['is_active'] else 'Inactive'}
"""
    
    message += "\n━━━━━━━━━━━━━━━━━━━━"
    return message

def get_system_stats_message(stats):
    """Generate system statistics message"""
    return f"""
<b>📊 SYSTEM STATISTICS</b>

━━━━━━━━━━━━━━━━━━━━
<b>User Statistics:</b>
• Total Users: {stats.get('total_users', 0):,}
• Active Today: {stats.get('active_today', 0):,}
• New Today: {stats.get('new_today', 0):,}

<b>Test Statistics:</b>
• Total Tests: {stats.get('total_tests', 0):,}
• Total Views Sent: {stats.get('total_views', 0):,}
• Avg Success Rate: {stats.get('success_rate', 0):.1f}%
• Tests Today: {stats.get('today_tests', 0):,}

<b>System Status:</b>
• TikTok Accounts: {stats.get('active_accounts', 0):,}
• Working Proxies: {stats.get('working_proxies', 0):,}
• System Uptime: {stats.get('uptime', '24h')}
• Queue Size: {stats.get('queue_size', 0):,}

━━━━━━━━━━━━━━━━━━━━
<b>Performance Metrics:</b>
• Views/Minute: 10,000
• Avg Test Duration: 45s
• System Load: 32%
• Memory Usage: 256MB/512MB

━━━━━━━━━━━━━━━━━━━━
<b>Last Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

def get_error_message(error, context=None):
    """Generate error message"""
    message = f"""
<b>❌ ERROR OCCURRED</b>

━━━━━━━━━━━━━━━━━━━━
<b>Error Type:</b> {type(error).__name__}
<b>Error Message:</b> {str(error)}
<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}
"""
    
    if context:
        message += f"\n<b>Context:</b> {context}"
    
    message += "\n━━━━━━━━━━━━━━━━━━━━\nPlease try again or contact support."
    
    return message

# Helper functions
def shorten_url(url, max_length=50):
    """Shorten URL for display"""
    if len(url) <= max_length:
        return url
    return url[:max_length-3] + "..."

def shorten_proxy(proxy, max_length=40):
    """Shorten proxy for display"""
    if len(proxy) <= max_length:
        return proxy
    
    # Hide credentials
    if '@' in proxy:
        parts = proxy.split('@')
        if len(parts) == 2:
            return f"***@{parts[1][:max_length-10]}..."
    
    return proxy[:max_length-3] + "..."

def generate_progress_bar(percentage, width=20):
    """Generate progress bar"""
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"

def calculate_estimated_time(views):
    """Calculate estimated completion time"""
    if views <= 1000:
        return "1-2 minutes"
    elif views <= 5000:
        return "3-5 minutes"
    elif views <= 10000:
        return "8-10 minutes"
    else:
        minutes = views / 10000
        return f"{minutes:.1f} minutes"

def calculate_remaining_time(current, total, speed):
    """Calculate remaining time"""
    if speed <= 0:
        return "Calculating..."
    
    remaining = total - current
    minutes = remaining / speed
    
    if minutes < 1:
        return f"{int(minutes*60)} seconds"
    else:
        return f"{minutes:.1f} minutes"

def format_date(date_string):
    """Format date string"""
    if not date_string:
        return "Never"
    
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime('%Y-%m-%d %H:%M')
    except:
        return date_string

def calculate_efficiency_score(success_rate, duration):
    """Calculate efficiency score"""
    # Higher success rate and shorter duration = higher score
    time_score = max(0, 10 - (duration / 60))  # Max 10 points for speed
    success_score = success_rate / 10  # Max 10 points for success
    
    return min(10, (time_score + success_score) / 2)