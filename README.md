# Emoji Nuker

**Emoji Nuker** is a lightweight utility that scans your project directory and removes all emojis from code files. It's especially useful for cleaning up emoji-laden comments, log messages, or commit artifacts in codebases before production or archiving.

## Features

- Recursively scans your project directory
- Removes emojis from common source code files:
  - `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.go`, `.rs`, `.html`, `.css`, `.json`, `.yml`, `.yaml`, `.sh`, `.md`, `.txt`
- **Smart Unicode Substitution**: Replace emojis with semantically relevant Unicode characters
- **Labeling Mode**: Replace emojis with descriptive labels like `[emoji:U+1F600]`
- **Interactive Mode**: Preview emoji substitutions without modifying files
- Standard Unix/Linux installation via Makefile
- Proper man page documentation
- Verbose output option for debugging
- Clean error handling and progress reporting
- GitHub Actions CI/CD workflow

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

# Examples of substitutions:
# 🚀 → ↑ (rocket to up arrow)
# ✅ → ✓ (green checkmark to Unicode checkmark)
# ❌ → ✗ (red cross to Unicode cross mark)
# 🔥 → 火 (fire emoji to CJK fire radical)
# ⚠ → ! (warning to exclamation mark)
# ⭐ → * (star to asterisk)
# ➡ → → (right arrow emoji to Unicode arrow)
# 🔺 → ▲ (red triangle up to Unicode triangle)
# 🔻 → ▼ (red triangle down to Unicode triangle)
# 1️⃣ → 1 (number)
# 🅰 → A (letter)
# Note: Diagonal arrows (↗ ↘ ↙ ↖) and up-down arrows (↕ ↔) are NOT replaced
```

### Labeling Mode
```bash
# Replace emojis with descriptive labels
emoji-nuker --label /path/to/project
emoji-nuker --label myfile.py
```

# Examples:
# 😀 → [emoji:U+1F600]
# 🚀 → [emoji:U+1F680]
# ✅ → [emoji:U+2705]
```

### Color Substitution Mode
```bash
# Replace emojis with colored Unicode alternatives
emoji-nuker --substitute --color /path/to/project
emoji-nuker --substitute --color myfile.py
```

# Examples with color:
# ✅ → ✓ (green checkmark)
# ❌ → ✗ (red cross mark)
# ⚠ → ! (yellow warning)
# 🔥 → 火 (red fire symbol)
```

### Combined Modes
```bash
# Use substitutions where available, label the rest
emoji-nuker --substitute --label /path/to/project

# Preview what would be substituted (no file changes)
emoji-nuker --interactive /path/to/project
```

### Other Options
```bash
# Show help
emoji-nuker --help

# Show version
emoji-nuker --version
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

### Testing
```bash
make test
```

### Checking Dependencies
```bash
make check-deps
```

### Available Make Targets
```bash
make help
```

### Testing

The project includes comprehensive testing through GitHub Actions:

- **Validation Tests**: Ensure no emoji characters are used in substitutions
- **Substitution Tests**: Verify key emoji-to-Unicode mappings work correctly
- **Pattern Tests**: Confirm emoji detection accuracy and Unicode symbol safety
- **Arrow Tests**: Verify diagonal arrows and up-down arrows are not replaced
- **Mode Tests**: Test all operation modes (substitute, label, interactive, color)
- **Smart Builder Tests**: Validate emoticon conversion and context-aware substitutions

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
print("Hello World! ↑")

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
│   └── emoji-nuker       # Main Python script
├── man/
│   └── emoji-nuker.1     # Manual page
├── .github/
│   └── workflows/
│       └── test.yml      # CI/CD workflow
├── test_emoji_input.py   # Test file for CI validation
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore            # Git ignore patterns
```

## Unicode Substitution Philosophy

The emoji-nuker follows a strict principle: **emoji characters should never be replaced with other emoji characters**. Instead, it substitutes emojis with appropriate Unicode symbols that are outside the emoji ranges.

### Key Distinctions:
- **Emoji Characters**: Characters officially designated as emojis (e.g., ✅, ❌, 🔥)
- **Unicode Symbols**: Regular Unicode characters outside emoji ranges (e.g., ✓, ✗, 火)

This ensures that substitutions don't introduce new emoji characters while maintaining semantic meaning.

## Unicode Substitution Examples

The tool includes mappings for common emojis using safe Unicode symbols:

| Emoji | Unicode Substitution | Category | Notes |
|-------|---------------------|----------|-------|
| 🚀 | ↑ | Symbols | Rocket to Unicode up arrow (U+2191) |
| ✅ | ✓ | Status | Green checkmark to Unicode checkmark (U+2713) |
| ❌ | ✗ | Status | Red cross to Unicode cross mark (U+2717) |
| 🔥 | 火 | Symbols | Fire emoji to CJK fire radical (U+706B) |
| ⚠ | ! | Status | Warning to exclamation mark |
| ⭐ | * | Symbols | Star to asterisk |
| ➡ | → | Arrows | Right arrow emoji to Unicode arrow (U+2192) |
| 🔺 | ▲ | Triangles | Red triangle up to Unicode triangle (U+25B2) |
| 🔻 | ▼ | Triangles | Red triangle down to Unicode triangle (U+25BC) |
| 1️⃣ | 1 | Numbers | Number emojis to digits |
| 🅰 | A | Letters | Letter emojis to letters |
| 💯 | 100 | Numbers | Hundred points to "100" |
| 😀 | :D | Emoticons | Smileys to text emoticons |
| 😊 | :) | Emoticons | Happy face to smile |
| 😉 | ;) | Emoticons | Winking face to wink |

### Important: Arrow Symbol Distinction

The tool correctly distinguishes between emoji characters and regular Unicode symbols:

**Unicode Symbols (NOT replaced):**
- Diagonal arrows: ↗ ↘ ↙ ↖ (U+2197, U+2198, U+2199, U+2196)
- Up-down arrows: ↕ ↔ (U+2195, U+2194)  
- Regular arrows: ← → ↑ ↓ (U+2190, U+2192, U+2191, U+2193)

**Emoji Characters (replaced):**
- Right arrow emoji: ➡ → → (U+27A1)
- Triangle emojis: 🔺 → ▲, 🔻 → ▼ (U+1F53A, U+1F53B)

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
