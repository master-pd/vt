#!/usr/bin/env python3
"""
VT BOT - TikTok View Bot Ultra Pro
Author: MASTER (RANA)
Team: MAR PD
Version: 4.0.0
"""

import os
import sys
import asyncio
import signal
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from core.vt_engine import VTEngine
from ui.vt_terminal import VTTerminal
from ui.vt_banner import VTBanner
from utils.vt_logger import VTLogger

class VTBot:
    """Main VT Bot Application"""
    
    def __init__(self):
        self.logger = VTLogger()
        self.banner = VTBanner()
        self.terminal = VTTerminal()
        self.engine = None
        self.running = False
        
    async def initialize(self):
        """Initialize the bot"""
        try:
            # Show banner
            self.banner.show_main_banner()
            
            # Initialize engine
            self.engine = VTEngine()
            await self.engine.initialize()
            
            self.logger.success("VT Bot initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
    
    async def start(self):
        """Start the bot"""
        if not await self.initialize():
            return
        
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start main menu
            await self.main_menu()
            
        except KeyboardInterrupt:
            await self.shutdown()
        except Exception as e:
            self.logger.error(f"Runtime error: {e}")
            await self.shutdown()
    
    async def main_menu(self):
        """Main menu loop"""
        while self.running:
            try:
                choice = await self.terminal.show_main_menu()
                
                if choice == "1":
                    await self.start_view_sending()
                elif choice == "2":
                    await self.manage_accounts()
                elif choice == "3":
                    await self.manage_proxies()
                elif choice == "4":
                    await self.show_statistics()
                elif choice == "5":
                    await self.engine.settings_menu()
                elif choice == "6":
                    await self.shutdown()
                    break
                else:
                    self.logger.warning("Invalid choice!")
                    
            except KeyboardInterrupt:
                await self.shutdown()
                break
    
    async def start_view_sending(self):
        """Start view sending process"""
        try:
            # Get video URL
            video_url = await self.terminal.get_video_url()
            if not video_url:
                return
            
            # Get view count
            view_count = await self.terminal.get_view_count()
            if not view_count:
                return
            
            # Start sending views
            await self.engine.start_view_sending(video_url, view_count)
            
        except Exception as e:
            self.logger.error(f"View sending error: {e}")
    
    async def manage_accounts(self):
        """Manage TikTok accounts"""
        await self.engine.account_manager.menu()
    
    async def manage_proxies(self):
        """Manage proxies"""
        await self.engine.proxy_manager.menu()
    
    async def show_statistics(self):
        """Show statistics"""
        await self.engine.show_statistics()
    
    def signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        asyncio.create_task(self.shutdown())
    
    async def shutdown(self):
        """Graceful shutdown"""
        if not self.running:
            return
        
        self.running = False
        self.logger.info("Shutting down VT Bot...")
        
        if self.engine:
            await self.engine.shutdown()
        
        self.logger.success("VT Bot shutdown complete!")
        sys.exit(0)

def main():
    """Main function"""
    try:
        # Create event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run bot
        bot = VTBot()
        loop.run_until_complete(bot.start())
        
    except KeyboardInterrupt:
        print("\n\nVT Bot terminated by user!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()