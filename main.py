#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN APPLICATION ENTRY POINT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import sys
import argparse
from terminal.interface import TerminalInterface
from telegram.bot_core import TelegramBot
from config import Config
from utils.logger import system_logger

def show_header():
    """Display application header"""
    border = "═" * Config.TERMINAL_WIDTH
    title = Config.PROJECT_NAME.center(Config.TERMINAL_WIDTH)
    version = f"Version {Config.VERSION}".center(Config.TERMINAL_WIDTH)
    author = f"Author: {Config.AUTHOR}".center(Config.TERMINAL_WIDTH)
    team = f"Team: {Config.TEAM}".center(Config.TERMINAL_WIDTH)
    
    header = f"\n{border}\n{title}\n{border}\n{version}\n{author}\n{team}\n{border}\n"
    print(header)
    
    system_logger.info(f"Starting {Config.PROJECT_NAME} v{Config.VERSION}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description=Config.PROJECT_NAME)
    
    parser.add_argument(
        '--mode', 
        choices=['terminal', 'bot', 'service', 'test'], 
        default='terminal',
        help='Application mode'
    )
    
    parser.add_argument(
        '--config', 
        type=str,
        help='Custom config file'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )
    
    args = parser.parse_args()
    
    # Show version and exit
    if args.version:
        show_header()
        sys.exit(0)
    
    # Set log level
    import logging
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Show header
    show_header()
    
    try:
        if args.mode == 'terminal':
            system_logger.info("Starting in TERMINAL mode")
            interface = TerminalInterface()
            interface.run()
            
        elif args.mode == 'bot':
            system_logger.info("Starting in BOT mode")
            
            if not Config.BOT_TOKEN:
                system_logger.error("Bot token not configured in config.py")
                print("\nERROR: Bot token not configured")
                print("Please add your bot token to config.py:")
                print(f"BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'")
                sys.exit(1)
            
            bot = TelegramBot()
            bot.run()
            
        elif args.mode == 'service':
            system_logger.info("Starting in SERVICE mode")
            print("Service mode not yet implemented")
            # TODO: Implement service/daemon mode
            
        elif args.mode == 'test':
            system_logger.info("Starting in TEST mode")
            print("Test mode - Running system checks...")
            # TODO: Implement system tests
            
        else:
            system_logger.error(f"Unknown mode: {args.mode}")
            print(f"Error: Unknown mode '{args.mode}'")
            sys.exit(1)
            
    except KeyboardInterrupt:
        system_logger.info("Application stopped by user")
        print("\n\nApplication stopped by user")
        
    except Exception as e:
        system_logger.error(f"Application error: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()