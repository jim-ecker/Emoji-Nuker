# Emoji Nuker

**Emoji Nuker** is a lightweight utility that scans your project directory and removes all emojis from code files. It's especially useful for cleaning up emoji-laden comments, log messages, or commit artifacts in codebases before production or archiving.

## Features

- Recursively scans your project directory
- Removes emojis from common source code files:
  - `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.go`, `.rs`, `.html`, `.css`, `.json`, `.yml`, `.yaml`, `.sh`, `.md`, `.txt`
- Standard Unix/Linux installation via Makefile
- Proper man page documentation
- Verbose output option for debugging
- Clean error handling and progress reporting

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

```bash
# Basic usage
emoji-nuker /path/to/your/project

# Clean current directory
emoji-nuker .

# Verbose output
emoji-nuker --verbose /path/to/project

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

## Supported File Types

The tool processes files with the following extensions:
- **Programming Languages**: `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.rb`, `.go`, `.rs`
- **Web Technologies**: `.html`, `.css`, `.json`
- **Configuration**: `.yml`, `.yaml`
- **Documentation**: `.sh`, `.md`, `.txt`

## Examples

### Before
```python
# This is a test file with emojis 
print("Hello World! 👋")

def test_function():
    return "Testing emoji removal! "
```

### After
```python
# This is a test file with emojis 
print("Hello World! ")

def test_function():
    return "Testing emoji removal! "
```

## Project Structure

```
emoji-nuker/
├── Makefile          # Build and installation system
├── src/
│   └── emoji-nuker   # Main Python script
├── man/
│   └── emoji-nuker.1 # Manual page
├── README.md         # This file
├── LICENSE           # MIT License
└── .gitignore        # Git ignore patterns
```

## Why Emoji Nuker?

Because not every production system wants to parse 👋, ✅, or 💯.

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
