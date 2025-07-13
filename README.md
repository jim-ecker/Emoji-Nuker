# Emoji Nuker

**Emoji Nuker** is a lightweight utility that scans your project directory and removes all emojis from code files. It's especially useful for cleaning up emoji-laden comments, log messages, or commit artifacts in codebases before production or archiving.

## Features

- Recursively scans your project directory
- Removes emojis from common source code files:
  - `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.go`, `.rs`, `.html`, `.css`, `.json`, `.yml`, `.yaml`, `.sh`, `.md`, `.txt`
- **Smart Unicode Substitution**: Replace emojis with semantically relevant Unicode characters
- **Historical Precedence Architecture**: Respects the original Unicode designation of characters
- **Labeling Mode**: Replace emojis with descriptive labels like `[emoji:U+1F600]`
- **Interactive Mode**: Preview emoji substitutions without modifying files
- **Color Mode**: Apply colored Unicode substitutions with ANSI color codes
- Standard Unix/Linux installation via Makefile
- Proper man page documentation
- Verbose output option for debugging
- Clean error handling and progress reporting
- GitHub Actions CI/CD workflow

## Historical Precedence Architecture

Emoji Nuker implements a **historical precedence architecture** that solves the fundamental set theory problem of characters being both Unicode symbols and emojis. The core principle is:

> **Characters that existed as Unicode symbols before emoji designation are treated as Unicode symbols, not emojis.**

### The Problem

Many characters exist in both Unicode symbol ranges and emoji ranges. For example:
- `*` (U+002A) is both an ASCII character and part of keycap emoji sequences like `*️⃣`
- `ℹ` (U+2139) was a Unicode symbol (Unicode 3.0) before becoming an emoji (Emoji 1.0)
- `→` (U+2192) is a Unicode arrow symbol, while `➡` (U+27A1) is an emoji arrow

### The Solution

The historical precedence architecture uses a `PRE_EMOJI_UNICODE_SYMBOLS` set containing characters that existed as Unicode symbols before emoji designation. The `is_emoji_for_replacement()` function implements this precedence rule:

```python
def is_emoji_for_replacement(char: str) -> bool:
    """Check if a character should be treated as an emoji for replacement purposes."""
    if len(char) != 1:
        return False
    
    codepoint = ord(char)
    
    # Historical precedence: if it was a Unicode symbol first, treat it as such
    if codepoint in PRE_EMOJI_UNICODE_SYMBOLS:
        return False
    
    # Otherwise, check if it's in the emoji ranges
    return codepoint in emoji_chars
```

### Pre-Emoji Unicode Symbols

The following characters are **preserved** (not replaced) because they existed as Unicode symbols before emoji designation:

| Symbol | Unicode | Description | Historical Context |
|--------|---------|-------------|-------------------|
| `*` | U+002A | Asterisk | ASCII → keycap emoji component |
| `#` | U+0023 | Hash/Number Sign | ASCII → keycap emoji component |
| `ℹ` | U+2139 | Information Source | Unicode 3.0 → Emoji 1.0 |
| `™` | U+2122 | Trade Mark Sign | Unicode 1.1 → Emoji 1.0 |
| `©` | U+00A9 | Copyright Sign | Unicode 1.1 → Emoji 1.0 |
| `®` | U+00AE | Registered Sign | Unicode 1.1 → Emoji 1.0 |
| `←` | U+2190 | Leftwards Arrow | Unicode 1.1 |
| `→` | U+2192 | Rightwards Arrow | Unicode 1.1 |
| `↑` | U+2191 | Upwards Arrow | Unicode 1.1 |
| `↓` | U+2193 | Downwards Arrow | Unicode 1.1 |
| `↗` | U+2197 | North East Arrow | Unicode 1.1 |
| `↘` | U+2198 | South East Arrow | Unicode 1.1 |
| `↙` | U+2199 | South West Arrow | Unicode 1.1 |
| `↖` | U+2196 | North West Arrow | Unicode 1.1 |
| `↕` | U+2195 | Up Down Arrow | Unicode 1.1 |
| `↔` | U+2194 | Left Right Arrow | Unicode 1.1 |
| `✓` | U+2713 | Check Mark | Unicode 1.1 |
| `✗` | U+2717 | Ballot X | Unicode 1.1 |
| `√` | U+221A | Square Root | Unicode 1.1 |
| `×` | U+00D7 | Multiplication Sign | Unicode 1.1 |
| `!` | U+0021 | Exclamation Mark | ASCII |
| `火` | U+706B | CJK Fire Radical | Unicode 1.1 |

### Emoji-First Characters

Only characters that were **emoji-first** (designed as emojis from the start) are replaced:

| Emoji | Unicode | Replacement | Description |
|-------|---------|-------------|-------------|
| `✅` | U+2705 | `✓` | Green checkmark → Unicode checkmark |
| `❌` | U+274C | `✗` | Red cross → Unicode cross mark |
| `🔥` | U+1F525 | `火` | Fire emoji → CJK fire radical |
| `⚠` | U+26A0 | `!` | Warning sign → Exclamation mark |
| `⭐` | U+2B50 | `*` | Star → Asterisk |
| `➡` | U+27A1 | `→` | Right arrow emoji → Unicode arrow |
| `🔺` | U+1F53A | `▲` | Red triangle up → Unicode triangle |
| `🔻` | U+1F53B | `▼` | Red triangle down → Unicode triangle |
| `🚀` | U+1F680 | `▲` | Rocket → Up arrow |
| `😀` | U+1F600 | `:D` | Grinning face → Emoticon |

### Special Case: Unicode-First Characters That Later Became Emojis

Some characters present a unique historical case: they were originally added to Unicode as regular text characters but later became emojis. These characters are treated as **emojis for replacement** because they were designed as emoji-style visual elements, even though they predate the official emoji standard.

| Character | Unicode | Added to Unicode | Became Emoji | Treatment | Reason |
|-----------|---------|------------------|--------------|-----------|---------|
| `🅰` | U+1F170 | Unicode 6.0 (Oct 2010) | Emoji 1.0 (Aug 2015) | **Replaced** | Designed as emoji-style button |
| `🅱` | U+1F171 | Unicode 6.0 (Oct 2010) | Emoji 1.0 (Aug 2015) | **Replaced** | Designed as emoji-style button |

**Key Distinction**: Unlike true pre-emoji Unicode symbols (like `→` or `*`), these characters were designed from the start as visual, emoji-style elements in the "Enclosed Alphanumeric Supplement" block. They were intended to represent colored buttons and visual indicators, not traditional text symbols. Therefore, they are treated as emojis for replacement purposes despite predating the emoji standard by 5 years.

This maintains the principle that characters designed for emoji-style visual representation should be replaced, while preserving traditional Unicode symbols that have semantic meaning beyond visual representation.

### Why This Matters

This architecture ensures:
1. **Semantic Consistency**: Characters retain their original meaning
2. **Tool Compatibility**: emoji-nuker's own output uses safe Unicode symbols
3. **Predictable Behavior**: Clear rules for what gets replaced
4. **Unicode Respect**: Honors the historical development of Unicode

## Installation

### Quick Install (User Directory)
```bash
make install-user
```

This installs the tool to `~/.local/bin/emoji-nuker` and adds the man page to `~/.local/share/man/man1/`.

### System-wide Install (Requires sudo)
```bash
sudo make install
```

This installs the tool to `/usr/local/bin/emoji-nuker` and adds the man page to `/usr/local/share/man/man1/`.

### Manual Install
If you prefer to install manually:

```bash
# Make the script executable
chmod +x src/emoji-nuker

# Copy to your bin directory
cp src/emoji-nuker ~/.local/bin/
# or for system-wide: sudo cp src/emoji-nuker /usr/local/bin/

# Install man page
cp man/emoji-nuker.1 ~/.local/share/man/man1/
# or for system-wide: sudo cp man/emoji-nuker.1 /usr/local/share/man/man1/
```

## Usage

### Basic Usage
```bash
# Remove all emojis from a directory (default behavior)
emoji-nuker /path/to/your/project

# Remove emojis from a single file
emoji-nuker myfile.py

# Clean current directory
emoji-nuker .

# Verbose output
emoji-nuker --verbose /path/to/project
```

### Smart Substitution Mode
```bash
# Replace emojis with Unicode alternatives where possible
emoji-nuker --substitute /path/to/project
emoji-nuker --substitute myfile.py
```

### Labeling Mode
```bash
# Replace emojis with descriptive labels
emoji-nuker --label /path/to/project
emoji-nuker --label myfile.py
```

### Color Substitution Mode
```bash
# Replace emojis with colored Unicode alternatives
emoji-nuker --substitute --color /path/to/project
emoji-nuker --substitute --color myfile.py
```

### Interactive Mode
```bash
# Preview what would be substituted (no file changes)
emoji-nuker --interactive /path/to/project
```

### Combined Modes
```bash
# Use substitutions where available, label the rest
emoji-nuker --substitute --label /path/to/project
```

### Other Options
```bash
# Show help
emoji-nuker --help

# Show version
emoji-nuker --version
```

## Substitution Examples

### Historical Precedence in Action

**Pre-emoji Unicode symbols (preserved):**
```python
# These are NOT replaced (historical precedence)
print("Status: ✓ passed, ✗ failed")
print("Direction: ← → ↑ ↓ ↗ ↘ ↙ ↖ ↕ ↔")
print("Math: √ × ! Info: ℹ Trademark: ™")
print("Copyright: © Registered: ® Fire: 火")
print("ASCII: * #")
```

**Emoji-first characters (replaced):**
```python
# Before (emoji-first characters)
print("Status: ✅ Success, ❌ Failed")
print("Symbols: 🔥 Fire, ⚠ Warning, ⭐ Star")
print("Arrow: ➡ Right")
print("Triangles: 🔺 Up, 🔻 Down")
print("Rocket: 🚀")

# After (with --substitute)
print("Status: ✓ Success, ✗ Failed")
print("Symbols: 火 Fire, ! Warning, * Star")
print("Arrow: → Right")
print("Triangles: ▲ Up, ▼ Down")
print("Rocket: ▲")
```

### Emoticon Conversion

Face emojis are converted to text emoticons:
```python
# Before
print("Faces: 😀 😊 😉 😢")

# After
print("Faces: :D :) ;) :'(")
```

### Labeling Mode

When substitution isn't available, emojis are labeled:
```python
# Before
print("Complex emoji: 🧑‍💻")

# After (with --label)
print("Complex emoji: [emoji:U+1F9D1]")
```

## Uninstallation

### User Installation
```bash
make uninstall-user
```

### System-wide Installation
```bash
sudo make uninstall
```

## Development

### Building
```bash
make all
```

### Comprehensive Testing
```bash
make test
```

The Makefile includes a comprehensive test suite with 8 test categories:

1. **Basic Functionality**: Module loading and script validation
2. **Historical Precedence Architecture**: Tests all 22 pre-emoji Unicode symbols
3. **Emoji Detection**: Validates emoji-first character detection
4. **Command Line Options**: Tests all options (--help, --version, --verbose, --substitute, --interactive, --label, --color)
5. **File Processing Modes**: Tests all processing modes with real files
6. **Substitution Validation**: Ensures no emoji characters in substitutions
7. **File Type Support**: Tests multiple file extensions (.py, .js, .cpp, .md)
8. **Directory Processing**: Validates recursive directory processing

### Testing CI Workflow Locally
```bash
make test-ci
```

### Checking Dependencies
```bash
make check-deps
```

### Available Make Targets
```bash
make help
```

All available targets:
- `all` - Build the application (default)
- `install` - Install system-wide (requires sudo)
- `install-user` - Install to user directory
- `uninstall` - Uninstall system-wide (requires sudo)
- `uninstall-user` - Uninstall from user directory
- `test` - Run comprehensive tests
- `test-ci` - Test CI workflow locally
- `check-deps` - Check dependencies
- `clean` - Clean build artifacts
- `help` - Show help message

## Testing

The project includes comprehensive testing at multiple levels:

### Local Testing (Makefile)
- **Historical Precedence Validation**: Tests all 22 pre-emoji Unicode symbols are preserved
- **Emoji Detection Tests**: Validates emoji-first character detection for both single and multi-character emojis
- **Command Line Coverage**: Tests all command line options and their functionality
- **File Processing Tests**: Validates all processing modes (substitute, interactive, label, color, verbose)
- **File Type Coverage**: Tests supported file extensions (.py, .js, .cpp, .md, etc.)
- **Directory Processing**: Validates recursive directory scanning
- **Substitution Validation**: Ensures no emoji characters are used in substitutions
- **Architecture Validation**: Confirms historical precedence logic works correctly

### GitHub Actions (CI/CD)
- **Historical Precedence Architecture**: Comprehensive validation of the core architecture
- **Emoji Detection Tests**: Verifies emoji-first characters are correctly identified
- **Substitution Tests**: Validates key emoji-to-Unicode mappings
- **Mode Tests**: Tests all operation modes (substitute, label, interactive, color)
- **Smart Builder Tests**: Validates emoticon conversion and context-aware substitutions
- **Architecture Tests**: Confirms the historical precedence logic works correctly

### Test Coverage Summary
✓ Historical precedence architecture  
✓ Pre-emoji Unicode symbol preservation  
✓ Emoji-first character detection  
✓ All command line options  
✓ All processing modes  
✓ Substitution validation  
✓ File type support  
✓ Directory processing

## Supported File Types

The tool processes files with the following extensions:
- **Programming Languages**: `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.rb`, `.go`, `.rs`
- **Web Technologies**: `.html`, `.css`, `.json`
- **Configuration**: `.yml`, `.yaml`
- **Documentation**: `.sh`, `.md`, `.txt`

## Examples

### Before (with emojis)
```python
# This is a test file with emojis 🐍
print("Hello World! 🚀")

def test_function():
    return "Testing emoji removal! 🎉"

# Success indicators
status = "✅ All tests passed"
error = "❌ Permission denied"
```

### After (with --substitute)
```python
# This is a test file with emojis ?
print("Hello World! ▲")

def test_function():
    return "Testing emoji removal! *"

# Success indicators
status = "✓ All tests passed"
error = "✗ Permission denied"
```

### After (with --label)
```python
# This is a test file with emojis [emoji:U+1F40D]
print("Hello World! [emoji:U+1F680]")

def test_function():
    return "Testing emoji removal! [emoji:U+1F389]"

# Success indicators
status = "[emoji:U+2705] All tests passed"
error = "[emoji:U+274C] Permission denied"
```

## Project Structure

```
emoji-nuker/
├── Makefile              # Build and installation system
├── src/
│   ├── emoji-nuker       # Main Python script
│   └── emoji_lut.py      # Emoji lookup table with historical precedence
├── man/
│   └── emoji-nuker.1     # Manual page
├── .github/
│   └── workflows/
│       └── test.yml      # CI/CD workflow
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore            # Git ignore patterns
```

## Unicode Substitution Philosophy

The emoji-nuker follows a strict principle: **emoji characters should never be replaced with other emoji characters**. Instead, it substitutes emojis with appropriate Unicode symbols that are outside the emoji ranges.

The **historical precedence architecture** ensures that characters are treated according to their original Unicode designation, solving the set theory problem of characters being both Unicode symbols and emojis.

## Why Emoji Nuker?

Because not every production system wants to parse 🐍, 🚀, or 😅.

## License

MIT License – use freely, modify wildly, share generously.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make test`
5. Submit a pull request

## Troubleshooting

### "Command not found" after installation
Make sure your PATH includes the installation directory:
- For user install: `~/.local/bin`
- For system install: `/usr/local/bin`

### Permission denied errors
Some files may be read-only or require elevated permissions. The tool will skip these files and report them.

### Binary files
The tool automatically skips binary files to avoid corruption.

### CI/CD
The project includes GitHub Actions workflows that automatically test the emoji nuker on every push and pull request.
