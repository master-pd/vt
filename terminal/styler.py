# -*- coding: utf-8 -*-
"""
TERMINAL STYLER
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

class TerminalStyler:
    def __init__(self, width=80):
        self.width = width
        
    def line(self, char="─"):
        return char * self.width
    
    def border(self, char="═"):
        return char * self.width
    
    def center(self, text):
        return text.center(self.width)
    
    def left_pad(self, text, pad=4):
        return " " * pad + text
    
    def title(self, text):
        border = self.border("═")
        centered = self.center(text)
        return f"\n{border}\n{centered}\n{border}\n"
    
    def subtitle(self, text):
        return f"\n{self.center(f'【 {text} 】')}\n"
    
    def section(self, text):
        line = self.line("─")
        return f"\n{line}\n{self.center(text)}\n{line}"
    
    def menu_item(self, num, text):
        return f"[{num}] {text}"
    
    def info(self, key, value):
        return f"  • {key}: {value}"
    
    def success(self, message):
        return f"  ✓ {message}"
    
    def error(self, message):
        return f"  ✗ {message}"
    
    def warning(self, message):
        return f"  ⚠ {message}"
    
    def progress_bar(self, current, total, length=50):
        percent = current / total
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}] {percent:.1%}"
    
    def table_row(self, cells):
        col_width = self.width // len(cells)
        row = "│".join(str(cell).ljust(col_width)[:col_width] for cell in cells)
        return f"│{row}│"
    
    def table_header(self, headers):
        line = self.line("─")
        header = self.table_row(headers)
        return f"\n{line}\n{header}\n{line}"
    
    def table_footer(self):
        return self.line("─")