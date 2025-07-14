#!/usr/bin/env python3
"""
Emoji Nuker - Remove emojis from code files in a project directory.

A lightweight utility that scans your project directory and removes all emojis
from code files. It's especially useful for cleaning up emoji-laden comments,
log messages, or commit artifacts in codebases before production or archiving.

Usage:
    emoji-nuker /path/to/project

Author: Your Name
License: MIT
"""

import os
import re
import sys
import argparse
import unicodedata
from pathlib import Path
from typing import Set, Pattern, Dict, List, Tuple, Optional

# Handle module import for both Python package and Unix-style installations
def setup_module_path():
    """Setup the Python path to find emoji_lut module."""
    # Try to import directly first (Python package installation)
    try:
        from emoji_lut import EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
        return EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
    except ImportError:
        # Unix-style installation: look for module in lib directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check for Unix-style installation paths
        possible_paths = [
            os.path.join(script_dir, '..', 'lib', 'emoji-nuker'),  # Relative to script
            '/usr/local/lib/emoji-nuker',  # System-wide
            '/usr/lib/emoji-nuker',  # Alternative system-wide
            os.path.expanduser('~/.local/lib/emoji-nuker'),  # User directory
        ]
        
        for lib_path in possible_paths:
            if os.path.exists(os.path.join(lib_path, 'emoji_lut.py')):
                sys.path.insert(0, lib_path)
                try:
                    from emoji_lut import EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
                    return EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
                except ImportError:
                    continue
        
        # If all else fails, try current directory (development)
        sys.path.insert(0, script_dir)
        try:
            from emoji_lut import EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
            return EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement
        except ImportError:
            print("Error: Could not find emoji_lut module. Please ensure proper installation.")
            sys.exit(1)

# Import the module
EMOJI_LUT, get_emoji_pattern, is_emoji_for_replacement = setup_module_path()


# Supported file extensions
CODE_EXTENSIONS: Set[str] = {
    ".py", ".js", ".ts", ".cpp", ".c", ".h", ".java", ".rb", ".go", ".rs",
    ".html", ".css", ".json", ".yml", ".yaml", ".sh", ".md", ".txt"
}

# Use the comprehensive emoji pattern from the LUT (covers all popular emoji tools)
EMOJI_PATTERN: Pattern = get_emoji_pattern()

# Emoticon to emoji mapping for smileys
EMOTICON_MAPPING: Dict[str, str] = {
    # Basic smileys
    "😀": ":D",     # grinning face
    "😁": ":D",     # beaming face with smiling eyes
    "😂": ":D",     # face with tears of joy
    "😃": ":D",     # grinning face with big eyes
    "😄": ":D",     # grinning face with smiling eyes
    "😅": ":)",     # grinning face with sweat
    "😆": ":D",     # grinning squinting face
    "😇": "O:)",    # smiling face with halo
    "😈": ">:)",    # smiling face with horns
    "😉": ";)",     # winking face
    "😊": ":)",     # smiling face with smiling eyes
    "😋": ":P",     # face savoring food
    "😌": ":)",     # relieved face
    "😍": ":*",     # smiling face with heart-eyes
    "😎": "8)",     # smiling face with sunglasses
    "😏": ":)",     # smirking face
    "😐": ":|",     # neutral face
    "😑": "-_-",    # expressionless face
    "😒": ":/",     # unamused face
    "😓": ":(",     # downcast face with sweat
    "😔": ":(",     # pensive face
    "😕": ":(",     # confused face
    "😖": ":(",     # confounded face
    "😗": ":*",     # kissing face
    "😘": ":*",     # face blowing a kiss
    "😙": ":*",     # kissing face with smiling eyes
    "😚": ":*",     # kissing face with closed eyes
    "😛": ":P",     # face with tongue
    "😜": ";P",     # winking face with tongue
    "😝": ":P",     # squinting face with tongue
    "😞": ":(",     # disappointed face
    "😟": ":(",     # worried face
    "😠": ">:(",    # angry face
    "😡": ">:(",    # pouting face
    "😢": ":'(",    # crying face
    "😣": ":(",     # persevering face
    "😤": ">:(",    # face with steam from nose
    "😥": ":(",     # sad but relieved face
    "😦": ":(",     # frowning face with open mouth
    "😧": ":(",     # anguished face
    "😨": ":(",     # fearful face
    "😩": ":(",     # weary face
    "😪": ":(",     # sleepy face
    "😫": ":(",     # tired face
    "😬": ":S",     # grimacing face
    "😭": ":'(",    # loudly crying face
    "😮": ":O",     # face with open mouth
    "😯": ":O",     # hushed face
    "😰": ":(",     # anxious face with sweat
    "😱": ":O",     # face screaming in fear
    "😲": ":O",     # astonished face
    "😳": ":O",     # flushed face
    "😴": "(-_-)",  # sleeping face
    "😵": "X(",     # dizzy face
    "😶": ":|",     # face without mouth
    "😷": ":(",     # face with medical mask
    "🙂": ":)",     # slightly smiling face
    "🙃": ":)",     # upside-down face
    "🙄": ":/",     # face with rolling eyes
    "🤐": ":|",     # zipper-mouth face
    "🤑": "$_$",    # money-mouth face
    "🤒": ":(",     # face with thermometer
    "🤓": "8)",     # nerd face
    "🤔": ":/",     # thinking face
    "🤕": ":(",     # face with head-bandage
    "🤗": ":)",     # hugging face
    "🤠": ":)",     # cowboy hat face
    "🤡": ":)",     # clown face
    "🤢": ":(",     # nauseated face
    "🤣": ":D",     # rolling on the floor laughing
    "🤤": ":P",     # drooling face
    "🤥": ":(",     # lying face
    "🤧": ":(",     # sneezing face
    "🤨": ":/",     # face with raised eyebrow
    "🤩": ":*",     # star-struck
    "🤪": ":P",     # zany face
    "🤫": ":)",     # shushing face
    "🤬": ">:(",    # face with symbols on mouth
    "🤭": ":)",     # face with hand over mouth
    "🤮": ":(",     # face vomiting
    "🤯": ":O",     # exploding head
    "🥰": ":*",     # smiling face with hearts
    "🥱": ":(",     # yawning face
    "🥲": ":)",     # smiling face with tear
    "🥳": ":D",     # partying face
    "🥴": ":(",     # woozy face
    "🥵": ":(",     # hot face
    "🥶": ":(",     # cold face
    "🥺": ":(",     # pleading face
    "🦄": ":)",     # unicorn (sometimes used as smiley)
    "😺": ":)",     # grinning cat
    "😸": ":D",     # grinning cat with smiling eyes
    "😹": ":D",     # cat with tears of joy
    "😻": ":*",     # smiling cat with heart-eyes
    "😼": ":)",     # cat with wry smile
    "😽": ":*",     # kissing cat
    "🙀": ":O",     # weary cat
    "😿": ":(",     # crying cat
    "😾": ">:(",    # pouting cat
    # Additional variations
    "☺": ":)",      # smiling face (text style)
    "☹": ":(",      # frowning face (text style)
}

# Color mapping for Unicode substitutions
COLOR_MAPPING: Dict[str, str] = {
    "red": "\033[31m",
    "green": "\033[32m", 
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

# Base substitution patterns for different emoji categories
BASE_SUBSTITUTIONS: Dict[str, str] = {
    # Success/Status symbols
    "✅": "✓",  # check mark
    "❌": "✗",   # cross mark
    "⚠": "!",    # warning sign
    "ℹ": "i",    # information
    "🔴": "O",   # red circle
    "🟢": "O",   # green circle
    "🟡": "O",   # yellow circle
    "🔵": "O",   # blue circle
    "🟣": "O",   # purple circle
    "🟠": "O",   # orange circle
    "⚫": "O",   # black circle
    "⚪": "O",   # white circle
    
    # Arrows
    "➡": "→",  # right arrow
    "🔄": "R",  # refresh/reload
    "🔃": "R",  # clockwise arrows
    "🔁": "R",  # repeat
    "🔂": "R",  # repeat once
    
    # Common symbols
    "🚀": "▲",  # rocket
    "💡": "O",  # light bulb -> circle
    "🔧": "T",  # wrench -> T
    "⚡": "~",  # lightning -> tilde
    "🔥": "火",  # fire -> yangxi fire radical
    "💯": "100", # hundred points
    "🎯": "O",  # target
    "🎉": "*",  # party popper -> asterisk
    "🎊": "*",  # confetti -> asterisk
    "⭐": "*",  # star
    "🌟": "*",  # glowing star
    "💫": "*",  # dizzy star
    "✨": "*",  # sparkles
    
    # Numbers
    "1️⃣": "1", "2️⃣": "2", "3️⃣": "3", "4️⃣": "4", "5️⃣": "5",
    "6️⃣": "6", "7️⃣": "7", "8️⃣": "8", "9️⃣": "9", "0️⃣": "0",
    
    # Letters
    "🅰": "A", "🅱": "B", "🆎": "AB", "🆑": "CL", "🆒": "COOL",
    "🆓": "FREE", "🆔": "ID", "🆕": "NEW", "🆖": "NG", "🆗": "OK",
    "🆘": "SOS", "🆙": "UP", "🆚": "VS",
    
    # Geometric shapes
    "⬛": "#", "⬜": "[]", "◼": "#", "◻": "[]", "◾": "#", "◽": "[]",
    "▪": "#", "▫": "[]", "🔶": "<>", "🔷": "<>", "🔸": "<>", "🔹": "<>",
    "🔺": "▲", "🔻": "▼", "💠": "<>", "🔘": "O", "🔲": "[]", "🔳": "[]",
    
    # Time
    "⏰": "T",  # alarm clock -> T
    "⏱": "T",  # stopwatch -> T
    "⏲": "T",  # timer -> T
    "⌛": "T",  # hourglass -> T
    "⏳": "T",  # hourglass flowing -> T
    "🕐": "12", "🕑": "1", "🕒": "2", "🕓": "3", "🕔": "4",
    "🕕": "5", "🕖": "6", "🕗": "7", "🕘": "8", "🕙": "9",
    "🕚": "10", "🕛": "11",
    
    # Weather
    "☀": "O", "🌞": "O", "🌝": "O", "🌛": "O", "🌜": "O",
    "🌚": "O", "🌙": "O", "🌘": "O", "🌗": "O", "🌖": "O",
    "🌕": "O", "🌔": "O", "🌓": "O", "🌒": "O", "🌑": "O",
    "☁": "~", "⛅": "~", "⛈": "~", "🌤": "~", "🌥": "~",
    "🌦": "~", "🌧": "~", "⛆": "~", "🌨": "~", "🌩": "~",
    "🌪": "~", "🌫": "~", "🌬": "~", "☂": "|", "⛱": "|",
    "☔": "~", "⚡": "~", "❄": "*", "☃": "*", "⛄": "*",
    "☄": "*", "🌈": "~",
}


class SmartSubstitutionBuilder:
    """Intelligent substitution builder that creates substitutions based on Unicode properties."""
    
    def __init__(self):
        self.cache: Dict[str, Optional[str]] = {}
        self.color_enabled = False
        
    def enable_color(self, enabled: bool = True):
        """Enable or disable color output."""
        self.color_enabled = enabled
        
    def get_unicode_name(self, char: str) -> str:
        """Get the Unicode name for a character."""
        try:
            # For multi-character emojis, use the first character
            if len(char) > 1:
                return unicodedata.name(char[0])
            return unicodedata.name(char)
        except ValueError:
            return ""
    
    def extract_color_from_name(self, name: str) -> Optional[str]:
        """Extract color information from Unicode name."""
        name_lower = name.lower()
        
        # Direct color matches
        color_keywords = {
            "red": "red",
            "green": "green", 
            "yellow": "yellow",
            "blue": "blue",
            "purple": "magenta",
            "orange": "yellow",  # closest ANSI color
            "black": "white",    # use white for visibility
            "white": "white",
            "brown": "yellow",   # closest ANSI color
        }
        
        for keyword, color in color_keywords.items():
            if keyword in name_lower:
                return color
                
        # Context-based color inference
        if any(word in name_lower for word in ["check", "correct", "success", "ok"]):
            return "green"
        elif any(word in name_lower for word in ["cross", "error", "wrong", "x"]):
            return "red"
        elif any(word in name_lower for word in ["warning", "caution", "alert"]):
            return "yellow"
        elif any(word in name_lower for word in ["info", "information", "question"]):
            return "blue"
        
        return None
    
    def get_base_symbol(self, char: str, name: str) -> str:
        """Get the base symbol for an emoji based on its Unicode name."""
        name_lower = name.lower()
        
        # Check if we have a predefined substitution
        if char in BASE_SUBSTITUTIONS:
            return BASE_SUBSTITUTIONS[char]
        
        # Shape-based substitutions
        if "circle" in name_lower:
            return "O"
        elif "square" in name_lower:
            return "[]"
        elif "triangle" in name_lower:
            if "up" in name_lower or "pointing up" in name_lower:
                return "▲"
            elif "down" in name_lower or "pointing down" in name_lower:
                return "▼"
            else:
                return "▲"
        elif "diamond" in name_lower:
            return "<>"
        elif "star" in name_lower:
            return "*"
        elif "heart" in name_lower:
            return "<3"
        elif "arrow" in name_lower:
            if "right" in name_lower:
                return "→"
            elif "left" in name_lower:
                return "←"
            elif "up" in name_lower:
                return "↑"
            elif "down" in name_lower:
                return "↓"
            else:
                return "→"
        elif "cross" in name_lower or " x " in name_lower:
            return "✗"
        elif "check" in name_lower or "tick" in name_lower:
            return "✓"
        elif "warning" in name_lower:
            return "!"
        elif "information" in name_lower:
            return "i"
        elif "question" in name_lower:
            return "?"
        elif "exclamation" in name_lower:
            return "!"
        elif "plus" in name_lower or "add" in name_lower:
            return "+"
        elif "minus" in name_lower or "subtract" in name_lower:
            return "-"
        elif "multiply" in name_lower:
            return "×"
        elif "divide" in name_lower:
            return "÷"
        elif "equals" in name_lower:
            return "="
        elif "percent" in name_lower:
            return "%"
        elif "dollar" in name_lower:
            return "$"
        elif "euro" in name_lower:
            return "€"
        elif "pound" in name_lower:
            return "£"
        elif "yen" in name_lower:
            return "¥"
        elif "copyright" in name_lower:
            return "©"
        elif "registered" in name_lower:
            return "®"
        elif "trademark" in name_lower:
            return "™"
        elif "degree" in name_lower:
            return "°"
        elif "music" in name_lower or "note" in name_lower:
            return "♪"
        elif "phone" in name_lower or "telephone" in name_lower:
            return "[]"
        elif "mail" in name_lower or "envelope" in name_lower:
            return "[]"
        elif "clock" in name_lower or "time" in name_lower:
            return "T"
        elif "sun" in name_lower:
            return "O"
        elif "moon" in name_lower:
            return "O"
        elif "cloud" in name_lower:
            return "~"
        elif "rain" in name_lower:
            return "~"
        elif "snow" in name_lower:
            return "*"
        elif "fire" in name_lower:
            return "*"
        elif "water" in name_lower:
            return "~"
        elif "lightning" in name_lower or "bolt" in name_lower:
            return "~"
        elif "earth" in name_lower or "globe" in name_lower:
            return "O"
        elif "mountain" in name_lower:
            return "▲"
        elif "tree" in name_lower:
            return "T"
        elif "flower" in name_lower:
            return "*"
        elif "building" in name_lower:
            return "[]"
        elif "home" in name_lower or "house" in name_lower:
            return "[]"
        elif "car" in name_lower or "automobile" in name_lower:
            return "[]"
        elif "plane" in name_lower or "airplane" in name_lower:
            return ">"
        elif "ship" in name_lower or "boat" in name_lower:
            return ">"
        elif "train" in name_lower:
            return "="
        elif "bicycle" in name_lower or "bike" in name_lower:
            return "O"
        elif "bus" in name_lower:
            return "[]"
        elif "rocket" in name_lower:
            return "↑"
        elif "gear" in name_lower or "settings" in name_lower:
            return "O"
        elif "hammer" in name_lower:
            return "T"
        elif "wrench" in name_lower:
            return "T"
        elif "scissors" in name_lower:
            return "X"
        elif "key" in name_lower:
            return "[]"
        elif "lock" in name_lower:
            return "[]"
        elif "shield" in name_lower:
            return "[]"
        elif "gun" in name_lower or "pistol" in name_lower:
            return ">"
        elif "bow" in name_lower and "arrow" in name_lower:
            return ">"
        elif "sword" in name_lower:
            return "|"
        elif "axe" in name_lower:
            return "T"
        elif "pick" in name_lower:
            return "T"
        elif "balance scale" in name_lower:
            return "="
        elif "chains" in name_lower:
            return "~"
        elif "coffin" in name_lower:
            return "[]"
        elif "funeral urn" in name_lower:
            return "[]"
        elif "atom" in name_lower:
            return "O"
        elif "no entry" in name_lower:
            return "X"
        elif "radioactive" in name_lower:
            return "!"
        elif "biohazard" in name_lower:
            return "!"
        elif "snowman" in name_lower:
            return "*"
        elif "umbrella" in name_lower:
            return "|"
        elif "keyboard" in name_lower:
            return "[]"
        elif "chess" in name_lower:
            return "[]"
        
        # Default fallback for any remaining cases
        return "?"
    
    def build_substitution(self, emoji: str) -> Optional[str]:
        """Build a smart substitution for an emoji character."""
        if emoji in self.cache:
            return self.cache[emoji]
        
        # Check for emoticon mapping first
        if emoji in EMOTICON_MAPPING:
            substitution = EMOTICON_MAPPING[emoji]
            self.cache[emoji] = substitution
            return substitution
        
        # Get Unicode name
        name = self.get_unicode_name(emoji)
        if not name:
            self.cache[emoji] = None
            return None
        
        # Get base symbol
        base_symbol = self.get_base_symbol(emoji, name)
        
        # Apply color if enabled
        if self.color_enabled:
            color = self.extract_color_from_name(name)
            if color and color in COLOR_MAPPING:
                substitution = f"{COLOR_MAPPING[color]}{base_symbol}{COLOR_MAPPING['reset']}"
            else:
                substitution = base_symbol
        else:
            substitution = base_symbol
        
        self.cache[emoji] = substitution
        return substitution


class EmojiSubstitution:
    """Handles emoji detection and substitution with Unicode alternatives."""
    
    def __init__(self, substitute: bool = False, interactive: bool = False, label: bool = False, color: bool = False):
        self.substitute = substitute
        self.interactive = interactive
        self.label = label
        self.color = color
        self.substitutions_made: List[Tuple[str, str, str]] = []  # (emoji, unicode, file_path)
        self.emojis_found: Dict[str, List[str]] = {}  # emoji -> list of files
        
        # Initialize smart substitution builder
        self.builder = SmartSubstitutionBuilder()
        self.builder.enable_color(color)
    
    def find_emoji_substitution(self, emoji: str) -> Optional[str]:
        """Find a Unicode substitution for an emoji using smart builder."""
        return self.builder.build_substitution(emoji)
    
    def process_content(self, content: str, file_path: str) -> str:
        """Process content and either substitute, collect, or remove emojis."""
        if self.substitute:
            return self._substitute_emojis(content, file_path)
        elif self.interactive:
            return self._collect_emojis(content, file_path)
        else:
            # Default behavior: remove emojis
            return self._remove_emojis(content, file_path)
    
    def _find_emojis_for_replacement(self, content: str) -> List[str]:
        """Find all emojis in content that should be replaced using historical precedence."""
        emojis = []
        i = 0
        while i < len(content):
            char = content[i]
            if is_emoji_for_replacement(char):
                # Check for multi-character emoji sequences
                emoji_seq = char
                j = i + 1
                while j < len(content) and is_emoji_for_replacement(content[j]):
                    emoji_seq += content[j]
                    j += 1
                emojis.append(emoji_seq)
                i = j
            else:
                i += 1
        return emojis

    def _substitute_emojis(self, content: str, file_path: str) -> str:
        """Replace emojis with Unicode alternatives or label/remove."""
        new_content = content
        
        # Find all emojis in the content using historical precedence
        emojis = self._find_emojis_for_replacement(content)
        
        # Sort by length (longest first) to avoid partial replacements
        emojis.sort(key=len, reverse=True)
        
        for emoji in emojis:
            substitution = self.find_emoji_substitution(emoji)
            if substitution and substitution != emoji:
                new_content = new_content.replace(emoji, substitution)
                self.substitutions_made.append((emoji, substitution, file_path))
                print(f"\033[32m✓ Replaced '{emoji}' with '{substitution}' in {file_path}\033[0m")
            elif self.label:
                # Create label using Unicode codepoint
                if len(emoji) == 1:
                    label = f"[emoji:U+{ord(emoji):04X}]"
                else:
                    # For multi-character emojis, use first character's codepoint
                    label = f"[emoji:U+{ord(emoji[0]):04X}]"
                new_content = new_content.replace(emoji, label)
                self.substitutions_made.append((emoji, label, file_path))
                print(f"\033[36mℹ Labeled '{emoji}' as '{label}' in {file_path}\033[0m")
            else:
                new_content = new_content.replace(emoji, "")
                print(f"\033[33m⚠ Removed '{emoji}' (no substitution/label) from {file_path}\033[0m")
        
        return new_content
    
    def _remove_emojis(self, content: str, file_path: str) -> str:
        """Remove emojis from content (default behavior)."""
        emojis = self._find_emojis_for_replacement(content)
        
        # Sort by length (longest first) to avoid partial replacements
        emojis.sort(key=len, reverse=True)
        
        new_content = content
        for emoji in emojis:
            new_content = new_content.replace(emoji, "")
            print(f"\033[33m⚠ Removed '{emoji}' from {file_path}\033[0m")
        
        return new_content
    
    def _collect_emojis(self, content: str, file_path: str) -> str:
        """Collect emojis for later review without modifying content."""
        emojis = self._find_emojis_for_replacement(content)
        
        for emoji in emojis:
            if emoji not in self.emojis_found:
                self.emojis_found[emoji] = []
            if file_path not in self.emojis_found[emoji]:
                self.emojis_found[emoji].append(file_path)
        
        return content
    
    def show_substitution_summary(self):
        """Show summary of substitutions made."""
        if self.substitutions_made:
            print(f"\n\033[34m■ Substitution Summary:\033[0m")
            for emoji, substitution, file_path in self.substitutions_made:
                print(f"   '{emoji}' → '{substitution}' in {file_path}")
    
    def show_emoji_suggestions(self):
        """Show emojis found with potential substitutions."""
        if not self.emojis_found:
            return
        
        print(f"\n\033[34m■ Emojis Found (Smart Substitutions):\033[0m")
        for emoji, files in self.emojis_found.items():
            substitution = self.find_emoji_substitution(emoji)
            if substitution:
                print(f"\n\033[32m✓ '{emoji}' → '{substitution}'\033[0m")
            else:
                print(f"\n\033[33m⚠ '{emoji}' → (no substitution available)\033[0m")
            
            for file_path in files:
                print(f"   □ {file_path}")


def remove_emojis_from_file(file_path: Path, substitution_handler: EmojiSubstitution) -> bool:
    """
    Remove emojis from a single file.
    
    Args:
        file_path: Path to the file to process
        substitution_handler: Handler for emoji substitution logic
        
    Returns:
        True if the file was modified, False otherwise
    """
    try:
        # Read file content
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        
        # Process content based on substitution mode
        new_content = substitution_handler.process_content(content, str(file_path))
        
        # Only write if content changed
        if content != new_content:
            with file_path.open("w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"\033[32m✓ Cleaned: {file_path}\033[0m")
            return True
        else:
            print(f"\033[34mℹ No emojis found: {file_path}\033[0m")
            return False
            
    except UnicodeDecodeError:
        print(f"\033[33m⚠ Skipping binary file: {file_path}\033[0m")
        return False
    except PermissionError:
        print(f"\033[31m✗ Permission denied: {file_path}\033[0m")
        return False
    except Exception as e:
        print(f"\033[31m✗ Failed to process {file_path}: {e}\033[0m")
        return False


def clean_directory(root: Path, verbose: bool = False, substitution_handler: Optional[EmojiSubstitution] = None) -> tuple[int, int]:
    """
    Recursively clean all code files in a directory.
    
    Args:
        root: Root directory to scan
        verbose: Enable verbose output
        substitution_handler: Handler for emoji substitution logic
        
    Returns:
        Tuple of (files_processed, files_modified)
    """
    if substitution_handler is None:
        substitution_handler = EmojiSubstitution()
    
    files_processed = 0
    files_modified = 0
    
    if verbose:
        print(f"Scanning directory: {root}")
        print(f"Supported extensions: {', '.join(sorted(CODE_EXTENSIONS))}")
    
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in CODE_EXTENSIONS:
            files_processed += 1
            if remove_emojis_from_file(path, substitution_handler):
                files_modified += 1
    
    return files_processed, files_modified


def validate_no_emoji_in_substitutions():
    """Validate that no emoji characters are used in any substitutions."""
    violations = []
    
    # Check BASE_SUBSTITUTIONS
    for emoji, substitution in BASE_SUBSTITUTIONS.items():
        # Check each character in the substitution
        for char in substitution:
            if is_emoji_for_replacement(char):
                violations.append(f"BASE_SUBSTITUTIONS['{emoji}'] = '{substitution}' contains emoji character '{char}'")
                break
    
    # Check EMOTICON_MAPPING
    for emoji, substitution in EMOTICON_MAPPING.items():
        # Check each character in the substitution
        for char in substitution:
            if is_emoji_for_replacement(char):
                violations.append(f"EMOTICON_MAPPING['{emoji}'] = '{substitution}' contains emoji character '{char}'")
                break
    
    if violations:
        print("VALIDATION FAILED: Emoji characters found in substitutions:")
        for violation in violations:
            print(f"  - {violation}")
        return False
    else:
        print("VALIDATION PASSED: No emoji characters found in substitutions")
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Remove emojis from code files in a project directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  emoji-nuker /path/to/project           # Remove all emojis from directory
  emoji-nuker myfile.py                  # Remove emojis from single file
  emoji-nuker .                          # Clean current directory
  emoji-nuker --verbose /path            # Verbose output
  emoji-nuker --substitute /path         # Replace emojis with smart Unicode alternatives
  emoji-nuker --substitute --color /path # Replace with colored Unicode alternatives
  emoji-nuker --interactive /path        # Show emoji suggestions without modifying files
  emoji-nuker --label /path              # Replace emojis with a label like [emoji:U+XXXX] if no substitution exists
        """
    )
    
    parser.add_argument(
        "path",
        type=str,
        help="Path to a file or directory to process"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--substitute", "-s",
        action="store_true",
        help="Replace emojis with smart Unicode alternatives instead of removing them"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Show emoji suggestions without modifying files"
    )
    
    parser.add_argument(
        "--label", "-l",
        action="store_true",
        help="Replace emojis with a label like [emoji:U+XXXX] if no substitution exists"
    )
    
    parser.add_argument(
        "--color", "-c",
        action="store_true",
        help="Use colored Unicode substitutions (ANSI color codes)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="emoji-nuker 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Validate path
    target_path = Path(args.path)
    if not target_path.exists():
        print(f"\033[31m✗ Error: Path does not exist: {target_path}\033[0m")
        sys.exit(1)
    
    # Create substitution handler
    substitution_handler = EmojiSubstitution(
        substitute=args.substitute,
        interactive=args.interactive,
        label=args.label,
        color=args.color
    )
    
    # Process files
    try:
        if target_path.is_file():
            # Process single file
            if target_path.suffix in CODE_EXTENSIONS:
                files_processed = 1
                files_modified = 1 if remove_emojis_from_file(target_path, substitution_handler) else 0
            else:
                print(f"\033[33m⚠ Skipping unsupported file type: {target_path}\033[0m")
                files_processed = 0
                files_modified = 0
        else:
            # Process directory
            files_processed, files_modified = clean_directory(target_path, args.verbose, substitution_handler)
        
        print(f"\nSummary:")
        print(f"   Files processed: {files_processed}")
        print(f"   Files modified: {files_modified}")
        
        # Show appropriate summary based on mode
        if args.substitute:
            substitution_handler.show_substitution_summary()
        elif args.interactive:
            substitution_handler.show_emoji_suggestions()
        else:
            if files_modified > 0:
                print(f"\033[32m✓ Successfully removed emojis from {files_modified} files!\033[0m")
            else:
                print("\033[34mℹ No files were modified.\033[0m")
            
    except KeyboardInterrupt:
        print("\n\033[33m⚠ Operation cancelled by user\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[31m✗ Unexpected error: {e}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main() 