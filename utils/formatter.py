# -*- coding: utf-8 -*-
"""
FORMATTER - TEXT FORMATTING AND STYLING
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import textwrap
from typing import Dict, List, Union
from config import Config

class Formatter:
    def __init__(self, width: int = None):
        self.width = width or Config.TERMINAL_WIDTH
        self.colors = self._init_colors()
        
    def _init_colors(self) -> Dict:
        """Initialize color codes"""
        return {
            'reset': '\033[0m',
            'bold': '\033[1m',
            'dim': '\033[2m',
            'italic': '\033[3m',
            'underline': '\033[4m',
            'blink': '\033[5m',
            'reverse': '\033[7m',
            'hidden': '\033[8m',
            
            # Regular colors
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            
            # Bright colors
            'bright_black': '\033[90m',
            'bright_red': '\033[91m',
            'bright_green': '\033[92m',
            'bright_yellow': '\033[93m',
            'bright_blue': '\033[94m',
            'bright_magenta': '\033[95m',
            'bright_cyan': '\033[96m',
            'bright_white': '\033[97m',
            
            # Background colors
            'bg_black': '\033[40m',
            'bg_red': '\033[41m',
            'bg_green': '\033[42m',
            'bg_yellow': '\033[43m',
            'bg_blue': '\033[44m',
            'bg_magenta': '\033[45m',
            'bg_cyan': '\033[46m',
            'bg_white': '\033[47m',
            
            # Bright background colors
            'bg_bright_black': '\033[100m',
            'bg_bright_red': '\033[101m',
            'bg_bright_green': '\033[102m',
            'bg_bright_yellow': '\033[103m',
            'bg_bright_blue': '\033[104m',
            'bg_bright_magenta': '\033[105m',
            'bg_bright_cyan': '\033[106m',
            'bg_bright_white': '\033[107m',
        }
    
    def colorize(self, text: str, color: str = None, style: str = None) -> str:
        """Add color and style to text"""
        if not color and not style:
            return text
        
        codes = []
        if color and color in self.colors:
            codes.append(self.colors[color])
        if style and style in self.colors:
            codes.append(self.colors[style])
        
        if codes:
            return f"{''.join(codes)}{text}{self.colors['reset']}"
        
        return text
    
    def format_header(self, text: str, color: str = 'cyan', style: str = 'bold') -> str:
        """Format header text"""
        border = self.colorize("═" * self.width, color)
        centered = self.center_text(text)
        colored_text = self.colorize(centered, color, style)
        
        return f"\n{border}\n{colored_text}\n{border}\n"
    
    def format_section(self, text: str, color: str = 'blue') -> str:
        """Format section header"""
        border = self.colorize("─" * self.width, color)
        centered = self.center_text(text)
        colored_text = self.colorize(centered, color, 'bold')
        
        return f"\n{border}\n{colored_text}\n{border}"
    
    def format_subsection(self, text: str, color: str = 'yellow') -> str:
        """Format subsection"""
        border = self.colorize("─" * 40, color)
        centered = self.center_text(text, 40)
        colored_text = self.colorize(centered, color)
        
        return f"\n{border}\n{colored_text}"
    
    def format_info(self, label: str, value: str, 
                   label_color: str = 'green', value_color: str = 'white') -> str:
        """Format information line"""
        label_text = self.colorize(f"  • {label}:", label_color, 'bold')
        value_text = self.colorize(f" {value}", value_color)
        
        return f"{label_text}{value_text}"
    
    def format_success(self, message: str) -> str:
        """Format success message"""
        return self.colorize(f"  ✓ {message}", 'green', 'bold')
    
    def format_error(self, message: str) -> str:
        """Format error message"""
        return self.colorize(f"  ✗ {message}", 'red', 'bold')
    
    def format_warning(self, message: str) -> str:
        """Format warning message"""
        return self.colorize(f"  ⚠ {message}", 'yellow', 'bold')
    
    def format_note(self, message: str) -> str:
        """Format note message"""
        return self.colorize(f"  📌 {message}", 'cyan')
    
    def format_process(self, message: str) -> str:
        """Format process message"""
        return self.colorize(f"  ⚡ {message}", 'magenta')
    
    def format_result(self, label: str, value: str) -> str:
        """Format result line"""
        return self.colorize(f"  ▸ {label}: ", 'blue', 'bold') + self.colorize(value, 'white')
    
    def format_table(self, headers: List[str], rows: List[List], 
                    header_color: str = 'cyan', row_color: str = 'white') -> str:
        """Format data as table"""
        if not headers or not rows:
            return ""
        
        # Calculate column widths
        col_widths = [len(str(h)) + 2 for h in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                cell_len = len(str(cell)) + 2
                if cell_len > col_widths[i]:
                    col_widths[i] = cell_len
        
        # Ensure total width doesn't exceed terminal width
        total_width = sum(col_widths) + len(headers) - 1
        if total_width > self.width:
            # Reduce column widths proportionally
            ratio = self.width / total_width
            col_widths = [int(w * ratio) for w in col_widths]
        
        # Build table
        table_lines = []
        
        # Top border
        top_border = "┌" + "┬".join(["─" * w for w in col_widths]) + "┐"
        table_lines.append(self.colorize(top_border, 'white'))
        
        # Header row
        header_cells = []
        for i, header in enumerate(headers):
            header_cells.append(self.colorize(str(header).center(col_widths[i]), header_color, 'bold'))
        
        header_row = "│" + "│".join(header_cells) + "│"
        table_lines.append(header_row)
        
        # Separator
        separator = "├" + "┼".join(["─" * w for w in col_widths]) + "┤"
        table_lines.append(self.colorize(separator, 'white'))
        
        # Data rows
        for row in rows:
            row_cells = []
            for i, cell in enumerate(row):
                row_cells.append(self.colorize(str(cell).ljust(col_widths[i]), row_color))
            
            row_line = "│" + "│".join(row_cells) + "│"
            table_lines.append(row_line)
        
        # Bottom border
        bottom_border = "└" + "┴".join(["─" * w for w in col_widths]) + "┘"
        table_lines.append(self.colorize(bottom_border, 'white'))
        
        return "\n".join(table_lines)
    
    def format_progress_bar(self, current: int, total: int, 
                           length: int = 40, show_percentage: bool = True) -> str:
        """Format progress bar"""
        if total == 0:
            return ""
        
        percent = current / total
        filled_length = int(length * percent)
        
        bar = self.colorize("█" * filled_length, 'green') + \
              self.colorize("░" * (length - filled_length), 'dim')
        
        if show_percentage:
            percentage = f" {percent:.1%}"
            return f"[{bar}]{percentage}"
        
        return f"[{bar}]"
    
    def format_key_value_pairs(self, data: Dict, 
                              key_color: str = 'cyan', 
                              value_color: str = 'white') -> str:
        """Format key-value pairs"""
        lines = []
        max_key_length = max(len(str(k)) for k in data.keys()) if data else 0
        
        for key, value in data.items():
            key_str = self.colorize(str(key).rjust(max_key_length), key_color, 'bold')
            value_str = self.colorize(f" : {value}", value_color)
            lines.append(f"{key_str}{value_str}")
        
        return "\n".join(lines)
    
    def format_code_block(self, code: str, language: str = 'python') -> str:
        """Format code block"""
        border = self.colorize("┌" + "─" * (self.width - 2) + "┐", 'white')
        lang_label = self.colorize(f" {language} ", 'black', 'bg_white')
        code_lines = code.split('\n')
        
        formatted_lines = [border]
        formatted_lines.append(f"│{lang_label.ljust(self.width - 2)}│")
        formatted_lines.append(self.colorize("├" + "─" * (self.width - 2) + "┤", 'white'))
        
        for line in code_lines:
            if len(line) > self.width - 4:
                wrapped = textwrap.wrap(line, width=self.width - 4)
                for wrapped_line in wrapped:
                    formatted_lines.append(f"│ {wrapped_line.ljust(self.width - 4)} │")
            else:
                formatted_lines.append(f"│ {line.ljust(self.width - 4)} │")
        
        formatted_lines.append(self.colorize("└" + "─" * (self.width - 2) + "┘", 'white'))
        
        return "\n".join(formatted_lines)
    
    def format_list(self, items: List[str], 
                   bullet: str = '•', 
                   color: str = 'white',
                   indent: int = 2) -> str:
        """Format list"""
        lines = []
        indent_str = " " * indent
        
        for item in items:
            bullet_str = self.colorize(bullet, 'cyan')
            item_str = self.colorize(str(item), color)
            lines.append(f"{indent_str}{bullet_str} {item_str}")
        
        return "\n".join(lines)
    
    def format_columns(self, items: List[str], columns: int = 2) -> str:
        """Format items in columns"""
        if not items:
            return ""
        
        # Calculate column width
        max_item_length = max(len(str(item)) for item in items)
        col_width = max_item_length + 4
        
        # Ensure columns fit in terminal width
        while columns * col_width > self.width and columns > 1:
            columns -= 1
        
        # Create rows
        rows = []
        for i in range(0, len(items), columns):
            row_items = items[i:i + columns]
            row = ""
            
            for item in row_items:
                row += str(item).ljust(col_width)
            
            rows.append(row.rstrip())
        
        return "\n".join(rows)
    
    def center_text(self, text: str, width: int = None) -> str:
        """Center text within width"""
        if width is None:
            width = self.width
        
        return text.center(width)
    
    def wrap_text(self, text: str, width: int = None) -> str:
        """Wrap text to specified width"""
        if width is None:
            width = self.width
        
        return "\n".join(textwrap.wrap(text, width=width))
    
    def truncate_text(self, text: str, max_length: int, ellipsis: str = "...") -> str:
        """Truncate text with ellipsis"""
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(ellipsis)] + ellipsis
    
    def remove_colors(self, text: str) -> str:
        """Remove color codes from text"""
        import re
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in human readable format"""
        if seconds < 60:
            return self.colorize(f"{seconds:.1f}s", 'cyan')
        elif seconds < 3600:
            minutes = seconds / 60
            return self.colorize(f"{minutes:.1f}m", 'yellow')
        elif seconds < 86400:
            hours = seconds / 3600
            return self.colorize(f"{hours:.1f}h", 'green')
        else:
            days = seconds / 86400
            return self.colorize(f"{days:.1f}d", 'magenta')
    
    def format_file_size(self, bytes_size: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return self.colorize(f"{bytes_size:.2f} {unit}", 'blue')
            bytes_size /= 1024.0
        return self.colorize(f"{bytes_size:.2f} PB", 'blue')