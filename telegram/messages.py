# -*- coding: utf-8 -*-
"""
MESSAGE TEMPLATES
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

from config import Config

def get_welcome_message(user):
    return f"""
<b>{Config.PROJECT_NAME}</b>
<code>Version {Config.VERSION}</code>

━━━━━━━━━━━━━━━━━━━━
<b>Welcome, {user.first_name}!</b>

I am an advanced TikTok view testing system developed by <b>{Config.AUTHOR}</b> from <b>{Config.TEAM}</b>.

━━━━━━━━━━━━━━━━━━━━
<b>HOW TO USE:</b>
1. Send me a TikTok video URL
2. Select desired view count
3. System will start sending views

<b>FEATURES:</b>
• 10-1000 views per minute
• Instant processing
• Real-time monitoring
• Detailed analytics

━━━━━━━━━━━━━━━━━━━━
<b>Send me a TikTok video URL to begin.</b>
"""

INVALID_INPUT = """
<b>Invalid Input</b>

Please send a valid TikTok video URL.

Example:
https://www.tiktok.com/@username/video/1234567890

Or use the menu buttons below.
"""

REQUEST_VIDEO_URL = """
<b>Video URL Received</b>

Now select how many views you want to send:

━━━━━━━━━━━━━━━━━━━━
<b>Available Options:</b>
"""

TEST_STARTED = """
<b>Test Started Successfully</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test Details:</b>
• Test ID: <code>{test_id}</code>
• Video URL: {url}
• Target Views: {views}
• Estimated Time: {time}

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>Processing...</code>
"""

TEST_PROGRESS = """
<b>Test Progress</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test ID:</b> <code>{test_id}</code>
<b>Progress:</b> {progress_bar}
<b>Views Sent:</b> {sent}/{total}
<b>Speed:</b> {speed}/minute
<b>Success Rate:</b> {success_rate}%

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>Running</code>
"""

TEST_COMPLETED = """
<b>Test Completed</b>

━━━━━━━━━━━━━━━━━━━━
<b>Test ID:</b> <code>{test_id}</code>
<b>Video URL:</b> {url}
<b>Target Views:</b> {target}
<b>Views Sent:</b> {sent}
<b>Views Verified:</b> {verified}
<b>Success Rate:</b> {success_rate}%
<b>Duration:</b> {duration}s

━━━━━━━━━━━━━━━━━━━━
<b>Status:</b> <code>Completed</code>
"""

STATS_MESSAGE = """
<b>System Statistics</b>

━━━━━━━━━━━━━━━━━━━━
<b>Overall:</b>
• Total Tests: {total_tests}
• Total Views Sent: {total_views}
• Success Rate: {success_rate}%

<b>Today:</b>
• Tests Today: {today_tests}
• Views Today: {today_views}

<b>System:</b>
• Active Accounts: {active_accounts}
• System Uptime: {uptime}
• Queue Size: {queue_size}

━━━━━━━━━━━━━━━━━━━━
<b>Last Updated:</b> {timestamp}
"""

HELP_MESSAGE = """
<b>Help & Support</b>

━━━━━━━━━━━━━━━━━━━━
<b>COMMANDS:</b>
/start - Start bot
/help - Show this help
/stats - View statistics
/cancel - Cancel current test

<b>HOW TO USE:</b>
1. Send TikTok video URL
2. Select view count from menu
3. Wait for completion
4. View results

<b>SUPPORTED URL FORMATS:</b>
• https://www.tiktok.com/@user/video/123
• https://vm.tiktok.com/ABC123/
• https://vt.tiktok.com/XYZ456/

<b>VIEW LIMITS:</b>
• Minimum: 10 views
• Maximum: 10,000 views
• Speed: Up to 10,000/min

━━━━━━━━━━━━━━━━━━━━
<b>Need more help?</b>
Contact system administrator.
"""

ERROR_MESSAGE = """
<b>Error Occurred</b>

━━━━━━━━━━━━━━━━━━━━
<b>Error:</b> {error}
<b>Time:</b> {time}

━━━━━━━━━━━━━━━━━━━━
Please try again or contact support.
"""

def format_progress_bar(percent, width=20):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent:.1f}%"