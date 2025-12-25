# -*- coding: utf-8 -*-
"""
TERMINAL INTERFACE
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import sys
import time
from .styler import TerminalStyler
from config import Config

class TerminalInterface:
    def __init__(self):
        self.styler = TerminalStyler(Config.TERMINAL_WIDTH)
        self.running = True
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        banner = self.styler.title(Config.PROJECT_NAME)
        banner += self.styler.center(f"Version {Config.VERSION}")
        banner += self.styler.center(f"By {Config.AUTHOR}")
        banner += self.styler.center(f"Team {Config.TEAM}")
        banner += self.styler.border()
        print(banner)
    
    def show_menu(self):
        menu = self.styler.section("MAIN MENU")
        menu += "\n"
        menu += self.styler.menu_item("1", "Start View Test") + "\n"
        menu += self.styler.menu_item("2", "Account Manager") + "\n"
        menu += self.styler.menu_item("3", "Proxy Manager") + "\n"
        menu += self.styler.menu_item("4", "Settings") + "\n"
        menu += self.styler.menu_item("5", "View Statistics") + "\n"
        menu += self.styler.menu_item("6", "Start Telegram Bot") + "\n"
        menu += self.styler.menu_item("0", "Exit") + "\n"
        menu += self.styler.line()
        print(menu)
    
    def get_input(self, prompt):
        return input(f"\n  {prompt}: ").strip()
    
    def show_test_config(self):
        config = self.styler.section("TEST CONFIGURATION")
        config += "\n"
        config += self.styler.info("Max Views/Minute", Config.MAX_VIEWS_PER_MINUTE) + "\n"
        config += self.styler.info("Min Views", Config.MIN_VIEWS) + "\n"
        config += self.styler.info("Max Views", Config.MAX_VIEWS) + "\n"
        config += self.styler.info("Request Delay", f"{Config.DELAY_BETWEEN_REQUESTS}s") + "\n"
        config += self.styler.line()
        print(config)
    
    def get_video_url(self):
        print(self.styler.section("VIDEO INPUT"))
        url = self.get_input("Enter TikTok Video URL")
        return url
    
    def get_view_count(self):
        print(self.styler.section("VIEW COUNT"))
        print(self.styler.info("Range", f"{Config.MIN_VIEWS} - {Config.MAX_VIEWS}"))
        while True:
            try:
                count = int(self.get_input("Enter View Count"))
                if Config.MIN_VIEWS <= count <= Config.MAX_VIEWS:
                    return count
                else:
                    print(self.styler.error(f"Please enter between {Config.MIN_VIEWS}-{Config.MAX_VIEWS}"))
            except ValueError:
                print(self.styler.error("Please enter a valid number"))
    
    def show_progress(self, current, total, speed=0):
        progress = self.styler.progress_bar(current, total)
        stats = f"  Progress: {current}/{total} | Speed: {speed}/min"
        print(f"\r{progress}{stats}", end="", flush=True)
    
    def show_results(self, test_id, views_sent, views_verified, success_rate, duration):
        results = self.styler.section("TEST RESULTS")
        results += "\n"
        results += self.styler.info("Test ID", test_id) + "\n"
        results += self.styler.info("Views Sent", views_sent) + "\n"
        results += self.styler.info("Views Verified", views_verified) + "\n"
        results += self.styler.info("Success Rate", f"{success_rate:.1f}%") + "\n"
        results += self.styler.info("Duration", f"{duration:.1f}s") + "\n"
        results += self.styler.line()
        print(results)
    
    def show_accounts_table(self, accounts):
        headers = ["ID", "Username", "Status", "Views Sent", "Last Used"]
        table = self.styler.table_header(headers)
        
        for acc in accounts:
            row = [
                acc.get('id', ''),
                acc.get('username', ''),
                acc.get('status', ''),
                acc.get('views_sent', 0),
                acc.get('last_used', 'Never')
            ]
            table += "\n" + self.styler.table_row(row)
        
        table += "\n" + self.styler.table_footer()
        print(table)
    
    def run(self):
        self.clear_screen()
        self.show_banner()
        
        while self.running:
            self.show_menu()
            choice = self.get_input("Select Option")
            
            if choice == "1":
                self.start_test_flow()
            elif choice == "2":
                self.account_manager()
            elif choice == "6":
                self.start_telegram_bot()
            elif choice == "0":
                self.exit_program()
            else:
                print(self.styler.error("Invalid option"))
                time.sleep(1)
    
    def start_test_flow(self):
        self.show_test_config()
        url = self.get_video_url()
        if not url:
            return
        
        count = self.get_view_count()
        
        print(self.styler.section("STARTING TEST"))
        print(self.styler.info("URL", url))
        print(self.styler.info("Target Views", count))
        print(self.styler.warning("Press Ctrl+C to stop"))
        print(self.styler.line())
        
        # Simulate test
        import random
        test_id = f"VT{random.randint(1000, 9999)}"
        views_sent = count
        views_verified = random.randint(int(count * 0.3), int(count * 0.7))
        success_rate = (views_verified / views_sent) * 100
        duration = random.uniform(30, 120)
        
        # Show progress
        for i in range(count):
            time.sleep(0.01)
            speed = random.randint(500, 1500)
            self.show_progress(i, count, speed)
        
        print("\n")
        self.show_results(test_id, views_sent, views_verified, success_rate, duration)
        self.get_input("Press Enter to continue")
    
    def account_manager(self):
        # Load accounts from JSON
        accounts = Config.load_json(Config.ACCOUNTS_FILE)
        account_list = accounts.get('accounts', [])
        
        print(self.styler.section("ACCOUNT MANAGER"))
        print(self.styler.info("Total Accounts", len(account_list)))
        self.show_accounts_table(account_list)
        
        print("\n" + self.styler.subtitle("Account Actions"))
        print(self.styler.menu_item("1", "Add New Account"))
        print(self.styler.menu_item("2", "Remove Account"))
        print(self.styler.menu_item("3", "Import Accounts"))
        print(self.styler.menu_item("4", "Export Accounts"))
        print(self.styler.menu_item("0", "Back"))
        
        choice = self.get_input("Select Action")
        # Implement account actions here
        
        self.get_input("Press Enter to continue")
    
    def start_telegram_bot(self):
        print(self.styler.section("TELEGRAM BOT"))
        print(self.styler.info("Status", "Starting..."))
        
        try:
            # Import and start bot
            from telegram.bot_core import TelegramBot
            bot = TelegramBot()
            print(self.styler.success("Bot started successfully"))
            print(self.styler.warning("Press Ctrl+C to stop bot"))
            
            # Keep running until interrupted
            import signal
            signal.signal(signal.SIGINT, lambda s, f: self.exit_program())
            while True:
                time.sleep(1)
                
        except ImportError as e:
            print(self.styler.error(f"Cannot start bot: {e}"))
        except Exception as e:
            print(self.styler.error(f"Bot error: {e}"))
        
        self.get_input("Press Enter to continue")
    
    def exit_program(self):
        print(self.styler.section("EXITING"))
        print(self.styler.center("Thank you for using VT View Tester"))
        print(self.styler.center(f"Author: {Config.AUTHOR}"))
        print(self.styler.center(f"Team: {Config.TEAM}"))
        print(self.styler.border())
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    import os
    interface = TerminalInterface()
    interface.run()