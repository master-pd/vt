# -*- coding: utf-8 -*-
"""
TELEGRAM BOT CORE
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import Config
from . import handlers
from . import keyboards
from . import messages

class TelegramBot:
    def __init__(self):
        self.token = Config.BOT_TOKEN
        self.app = None
        self.logger = logging.getLogger(__name__)
        
    async def start(self, update: Update, context):
        user = update.effective_user
        welcome = messages.get_welcome_message(user)
        
        keyboard = keyboards.get_main_menu()
        await update.message.reply_text(
            welcome,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    
    async def handle_message(self, update: Update, context):
        text = update.message.text
        
        if "tiktok.com" in text or "vt.tiktok.com" in text:
            await handlers.handle_video_url(update, context, text)
        else:
            await update.message.reply_text(
                messages.INVALID_INPUT,
                parse_mode='HTML'
            )
    
    async def handle_callback(self, update: Update, context):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("views_"):
            await handlers.handle_view_selection(query, context, data)
        elif data == "start_test":
            await handlers.handle_start_test(query, context)
        elif data == "stats":
            await handlers.handle_stats(query, context)
        elif data == "help":
            await handlers.handle_help(query, context)
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", handlers.handle_help_command))
        self.app.add_handler(CommandHandler("stats", handlers.handle_stats_command))
        
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
        
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
    
    def run(self):
        if not self.token:
            print("ERROR: Bot token not configured in config.py")
            return
        
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
        
        print("TELEGRAM BOT STARTED")
        print(f"Author: {Config.AUTHOR}")
        print(f"Team: {Config.TEAM}")
        print("Bot is running...")
        
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()