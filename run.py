#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN ENTRY POINT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import sys
import argparse
from terminal.interface import TerminalInterface
from telegram.bot_core import TelegramBot
from config import Config

def show_header():
    border = "═" * Config.TERMINAL_WIDTH
    title = Config.PROJECT_NAME.center(Config.TERMINAL_WIDTH)
    version = f"Version {Config.VERSION}".center(Config.TERMINAL_WIDTH)
    author = f"Author: {Config.AUTHOR}".center(Config.TERMINAL_WIDTH)
    team = f"Team: {Config.TEAM}".center(Config.TERMINAL_WIDTH)
    
    print(f"\n{border}")
    print(title)
    print(border)
    print(version)
    print(author)
    print(team)
    print(f"{border}\n")

def main():
    parser = argparse.ArgumentParser(description=Config.PROJECT_NAME)
    parser.add_argument('--mode', choices=['terminal', 'bot', 'both'], 
                       default='terminal', help='Run mode')
    parser.add_argument('--version', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    show_header()
    
    if args.version:
        print(f"{Config.PROJECT_NAME} v{Config.VERSION}")
        print(f"Author: {Config.AUTHOR}")
        print(f"Team: {Config.TEAM}")
        sys.exit(0)
    
    if args.mode == 'terminal':
        interface = TerminalInterface()
        interface.run()
    
    elif args.mode == 'bot':
        if not Config.BOT_TOKEN:
            print("ERROR: Bot token not configured in config.py")
            print("Please add your bot token to config.py")
            sys.exit(1)
        
        print("Starting Telegram Bot...")
        bot = TelegramBot()
        bot.run()
    
    elif args.mode == 'both':
        print("Starting both Terminal and Telegram Bot...")
        print("This feature requires threading implementation")
        print("Currently only single mode supported")
        sys.exit(1)

if __name__ == "__main__":
    main()