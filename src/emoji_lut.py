#!/usr/bin/env python3
"""
Comprehensive Emoji Lookup Table (LUT)
=====================================

This module provides a complete lookup table of all emoji characters that appear
in popular emoji copy/paste tools, based on Unicode TR51 (Technical Report #51)
and common implementations.

The LUT is organized by Unicode ranges and categories for efficient lookup and
validation of emoji characters.
"""

import re
from typing import Set, Dict, List, Tuple

# Characters that existed as Unicode symbols before emoji designation
# These should be treated as Unicode symbols, not emojis, for replacement purposes
PRE_EMOJI_UNICODE_SYMBOLS = {
    # ASCII characters that later became part of emoji sequences
    0x002A,  # * - Asterisk (ASCII → keycap emoji component)
    0x0023,  # # - Hash/Number Sign (ASCII → keycap emoji component)
    
    # Unicode symbols that later became emojis
    0x2139,  # ℹ - Information Source (Unicode 3.0 → Emoji 1.0)
    0x2122,  # ™ - Trade Mark Sign (Unicode 1.1 → Emoji 1.0)
    0x00A9,  # © - Copyright Sign (Unicode 1.1 → Emoji 1.0)
    0x00AE,  # ® - Registered Sign (Unicode 1.1 → Emoji 1.0)
    
    # Arrow symbols that are Unicode symbols, not emojis
    0x2190,  # ← - Leftwards Arrow
    0x2191,  # ↑ - Upwards Arrow  
    0x2192,  # → - Rightwards Arrow
    0x2193,  # ↓ - Downwards Arrow
    0x2194,  # ↔ - Left Right Arrow
    0x2195,  # ↕ - Up Down Arrow
    0x2196,  # ↖ - North West Arrow
    0x2197,  # ↗ - North East Arrow
    0x2198,  # ↘ - South East Arrow
    0x2199,  # ↙ - South West Arrow
    
    # Mathematical and technical symbols
    0x2713,  # ✓ - Check Mark
    0x2717,  # ✗ - Ballot X
    0x221A,  # √ - Square Root
    0x00D7,  # × - Multiplication Sign
    0x0021,  # ! - Exclamation Mark
    
    # Additional Unicode symbols that should not be treated as emojis
    0x706B,  # 火 - CJK Unified Ideograph (fire)
}

# Unicode Emoji Ranges (from Unicode TR51)
# These are the primary ranges where emoji characters are defined
EMOJI_RANGES = [
    # Emoticons block
    (0x1F600, 0x1F64F),  # Emoticons
    
    # Miscellaneous Symbols and Pictographs
    (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
    
    # Transport and Map Symbols
    (0x1F680, 0x1F6FF),  # Transport and Map Symbols
    
    # Supplemental Symbols and Pictographs
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    
    # Symbols and Pictographs Extended-A
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    
    # Regional Indicator Symbols (for flags)
    (0x1F1E0, 0x1F1FF),  # Regional Indicator Symbols
    
    # Variation Selectors
    (0xFE00, 0xFE0F),    # Variation Selectors
    
    # Skin Tone Modifiers
    (0x1F3FB, 0x1F3FF),  # Skin Tone Modifiers
]

# Additional emoji characters from other Unicode blocks
ADDITIONAL_EMOJI_CHARS = {
    # Dingbats block (selective)
    0x2702, 0x2705, 0x2708, 0x2709, 0x270A, 0x270B, 0x270C, 0x270D,
    0x270F, 0x2712, 0x2714, 0x2716, 0x271D, 0x2721, 0x2728, 0x2733,
    0x2734, 0x2744, 0x2747, 0x274C, 0x274E, 0x2753, 0x2754, 0x2755,
    0x2757, 0x2763, 0x2764, 0x2795, 0x2796, 0x2797, 0x27A1, 0x27B0,
    0x27BF,
    
    # Miscellaneous Symbols block (selective)
    0x2600, 0x2601, 0x2602, 0x2603, 0x2604, 0x260E, 0x2611, 0x2614,
    0x2615, 0x2618, 0x261D, 0x2620, 0x2622, 0x2623, 0x2626, 0x262A,
    0x262E, 0x262F, 0x2638, 0x2639, 0x263A, 0x2640, 0x2642, 0x2648,
    0x2649, 0x264A, 0x264B, 0x264C, 0x264D, 0x264E, 0x264F, 0x2650,
    0x2651, 0x2652, 0x2653, 0x2660, 0x2663, 0x2665, 0x2666, 0x2668,
    0x267B, 0x267E, 0x267F, 0x2692, 0x2693, 0x2694, 0x2695, 0x2696,
    0x2697, 0x2699, 0x269B, 0x269C, 0x26A0, 0x26A1, 0x26AA, 0x26AB,
    0x26B0, 0x26B1, 0x26BD, 0x26BE, 0x26C4, 0x26C5, 0x26C8, 0x26CE,
    0x26CF, 0x26D1, 0x26D3, 0x26D4, 0x26E9, 0x26EA, 0x26F0, 0x26F1,
    0x26F2, 0x26F3, 0x26F4, 0x26F5, 0x26F7, 0x26F8, 0x26F9, 0x26FA,
    0x26FD,
    
    # Geometric Shapes block (selective)
    0x25AA, 0x25AB, 0x25B6, 0x25C0, 0x25FB, 0x25FC, 0x25FD, 0x25FE,
    
    # Miscellaneous Technical block (selective)
    0x231A, 0x231B, 0x2328, 0x23CF, 0x23E9, 0x23EA, 0x23EB, 0x23EC,
    0x23ED, 0x23EE, 0x23EF, 0x23F0, 0x23F1, 0x23F2, 0x23F3, 0x23F8,
    0x23F9, 0x23FA,
    
    # Arrows block (selective)
    0x21A9, 0x21AA,
    
    # General Punctuation block (selective)
    0x203C, 0x2049,
    
    # Letterlike Symbols block (selective)
    # Note: 0x2122 (™) moved to PRE_EMOJI_UNICODE_SYMBOLS
    
    # Number Forms block (selective)
    0x2160, 0x2161, 0x2162, 0x2163, 0x2164, 0x2165, 0x2166, 0x2167,
    0x2168, 0x2169, 0x216A, 0x216B,
    
    # Enclosed Alphanumerics block (selective)
    0x24C2,
    
    # Enclosed Alphanumeric Supplement block (selective)
    0x1F170, 0x1F171, 0x1F17E, 0x1F17F, 0x1F18E, 0x1F191, 0x1F192,
    0x1F193, 0x1F194, 0x1F195, 0x1F196, 0x1F197, 0x1F198, 0x1F199,
    0x1F19A,
    
    # Mathematical Operators block (selective)
    0x2934, 0x2935,
    
    # Supplemental Arrows-B block (selective)
    0x2B05, 0x2B06, 0x2B07, 0x2B1B, 0x2B1C, 0x2B50, 0x2B55,
    
    # Latin-1 Supplement block (selective)
    0x00A9, 0x00AE,
}

# Keycap sequence components
KEYCAP_CHARS = {
    0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037,
    0x0038, 0x0039,  # 0-9
    0x0023,  # #
    0x002A,  # *
    0x20E3,  # Combining Enclosing Keycap
}

# Variation Selectors
VARIATION_SELECTORS = {
    0xFE0E,  # Variation Selector-15 (text style)
    0xFE0F,  # Variation Selector-16 (emoji style)
}

# Zero Width Joiner for emoji sequences
ZWJ = 0x200D

class EmojiLUT:
    """
    Comprehensive Emoji Lookup Table
    
    This class provides methods to:
    1. Check if a character is an emoji
    2. Generate comprehensive emoji patterns
    3. Validate emoji sequences
    4. Categorize emoji types
    """
    
    def __init__(self):
        self._emoji_chars = self._build_emoji_set()
        self._emoji_pattern = self._build_emoji_pattern()
    
    def _build_emoji_set(self) -> Set[int]:
        """Build a comprehensive set of all emoji character codepoints."""
        emoji_chars = set()
        
        # Add characters from emoji ranges
        for start, end in EMOJI_RANGES:
            for codepoint in range(start, end + 1):
                emoji_chars.add(codepoint)
        
        # Add additional emoji characters
        emoji_chars.update(ADDITIONAL_EMOJI_CHARS)
        
        # Note: Keycap characters (* and #) are not added to general emoji set
        # They are only emoji when part of keycap sequences like *️⃣
        
        # Add variation selectors
        emoji_chars.update(VARIATION_SELECTORS)
        
        # Add ZWJ
        emoji_chars.add(ZWJ)
        
        return emoji_chars
    
    def _build_emoji_pattern(self) -> re.Pattern:
        """Build a comprehensive regex pattern for all emoji characters."""
        # Convert codepoints to Unicode escape sequences
        ranges = []
        
        # Add emoji ranges
        for start, end in EMOJI_RANGES:
            ranges.append(f"\\U{start:08X}-\\U{end:08X}")
        
        # Add individual additional characters
        individual_chars = []
        for char in sorted(ADDITIONAL_EMOJI_CHARS):
            individual_chars.append(f"\\U{char:08X}")
        
        # Add variation selectors
        for char in sorted(VARIATION_SELECTORS):
            individual_chars.append(f"\\U{char:08X}")
        
        # Add ZWJ
        individual_chars.append(f"\\U{ZWJ:08X}")
        
        # Combine ranges and individual characters for regular emoji
        pattern_parts = ranges + individual_chars
        regular_emoji_pattern = "[" + "".join(pattern_parts) + "]+"
        
        # Keycap sequence pattern: [0-9*#] + optional variation selector + combining enclosing keycap
        keycap_pattern = r"[0-9*#]\uFE0F?\u20E3"
        
        # Combine both patterns with alternation
        combined_pattern = f"(?:{regular_emoji_pattern}|{keycap_pattern})"
        
        return re.compile(combined_pattern, re.UNICODE)
    
    def is_emoji_char(self, char: str) -> bool:
        """Check if a single character is an emoji character."""
        if len(char) != 1:
            return False
        return ord(char) in self._emoji_chars

    def is_emoji_for_replacement(self, char: str) -> bool:
        """
        Determine if a character should be treated as an emoji for replacement purposes.
        
        This implements the historical precedence rule:
        - Characters that existed as Unicode symbols before emoji designation 
          are treated as Unicode symbols, not emojis
        - Only characters designed as emojis or emoji-first characters are replaced
        - Keycap sequences (like 1️⃣) are treated as emojis for replacement
        """
        if len(char) == 1:
            # Single character logic
            codepoint = ord(char)
            
            # If it's a pre-emoji Unicode symbol, treat as Unicode symbol
            if codepoint in PRE_EMOJI_UNICODE_SYMBOLS:
                return False
            
            # Otherwise, check if it's in the emoji ranges/sets
            return codepoint in self._emoji_chars
        else:
            # Multi-character sequence logic
            # Check if it's a keycap sequence: [0-9*#] + optional variation selector + combining enclosing keycap
            if len(char) == 3 and char[0] in '0123456789*#' and char[1] == '\uFE0F' and char[2] == '\u20E3':
                return True
            elif len(char) == 2 and char[0] in '0123456789*#' and char[1] == '\u20E3':
                return True
            
            # For other multi-character sequences, check if they match the emoji pattern
            return self.is_emoji_sequence(char)
    
    def is_emoji_sequence(self, text: str) -> bool:
        """Check if a text string contains emoji characters."""
        return bool(self._emoji_pattern.search(text))
    
    def find_all_emoji(self, text: str) -> List[str]:
        """Find all emoji sequences in a text string."""
        return self._emoji_pattern.findall(text)
    
    def get_emoji_pattern(self) -> re.Pattern:
        """Get the compiled regex pattern for emoji detection."""
        return self._emoji_pattern
    
    def categorize_emoji(self, char: str) -> str:
        """Categorize an emoji character by its Unicode range."""
        if len(char) != 1:
            return "unknown"
        
        codepoint = ord(char)
        
        # Check ranges
        if 0x1F600 <= codepoint <= 0x1F64F:
            return "emoticons"
        elif 0x1F300 <= codepoint <= 0x1F5FF:
            return "miscellaneous_symbols_pictographs"
        elif 0x1F680 <= codepoint <= 0x1F6FF:
            return "transport_map_symbols"
        elif 0x1F900 <= codepoint <= 0x1F9FF:
            return "supplemental_symbols_pictographs"
        elif 0x1FA70 <= codepoint <= 0x1FAFF:
            return "symbols_pictographs_extended_a"
        elif 0x1F1E0 <= codepoint <= 0x1F1FF:
            return "regional_indicator"
        elif 0x1F3FB <= codepoint <= 0x1F3FF:
            return "skin_tone_modifier"
        elif codepoint in ADDITIONAL_EMOJI_CHARS:
            return "additional_emoji"
        elif codepoint in KEYCAP_CHARS:
            return "keycap"
        elif codepoint in VARIATION_SELECTORS:
            return "variation_selector"
        elif codepoint == ZWJ:
            return "zero_width_joiner"
        else:
            return "unknown"
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the emoji LUT."""
        return {
            "total_emoji_chars": len(self._emoji_chars),
            "emoji_ranges": len(EMOJI_RANGES),
            "additional_chars": len(ADDITIONAL_EMOJI_CHARS),
            "keycap_chars": len(KEYCAP_CHARS),
            "variation_selectors": len(VARIATION_SELECTORS),
        }


# Global instance for easy access
EMOJI_LUT = EmojiLUT()

# Convenience functions
def is_emoji(text: str) -> bool:
    """Check if text contains emoji characters."""
    return EMOJI_LUT.is_emoji_sequence(text)

def is_emoji_for_replacement(char: str) -> bool:
    """
    Determine if a character should be treated as an emoji for replacement purposes.
    
    This implements the historical precedence rule:
    - Characters that existed as Unicode symbols before emoji designation 
      are treated as Unicode symbols, not emojis
    - Only characters designed as emojis or emoji-first characters are replaced
    """
    return EMOJI_LUT.is_emoji_for_replacement(char)

def find_emoji(text: str) -> List[str]:
    """Find all emoji in text."""
    return EMOJI_LUT.find_all_emoji(text)

def get_emoji_pattern() -> re.Pattern:
    """Get the emoji regex pattern."""
    return EMOJI_LUT.get_emoji_pattern()

def categorize_emoji(char: str) -> str:
    """Categorize an emoji character."""
    return EMOJI_LUT.categorize_emoji(char)


if __name__ == "__main__":
    # Test the LUT
    lut = EmojiLUT()
    
    print("Emoji LUT Statistics:")
    stats = lut.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test some emoji
    test_emojis = ["😀", "🚀", "❤️", "🇺🇸", "👍🏽", "▲", "→", "✓"]
    
    print("\nTesting emoji detection:")
    for emoji in test_emojis:
        is_emoji_result = lut.is_emoji_sequence(emoji)
        category = lut.categorize_emoji(emoji[0]) if emoji else "unknown"
        print(f"  '{emoji}': emoji={is_emoji_result}, category={category}")
    
    # Test text with mixed content
    test_text = "Hello 😀 world! 🚀 Check this out: ✓ Done!"
    found_emojis = lut.find_all_emoji(test_text)
    print(f"\nFound emojis in '{test_text}': {found_emojis}") 