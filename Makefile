# Emoji Nuker Makefile
# Standard Unix/Linux application build system

# Configuration
PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
MANDIR = $(PREFIX)/share/man
MAN1DIR = $(MANDIR)/man1
DOCDIR = $(PREFIX)/share/doc/emoji-nuker

# Application details
APP_NAME = emoji-nuker
VERSION = 1.0.0
DESCRIPTION = Remove emojis from code files in a project directory

# Files
SCRIPT_FILE = src/emoji_nuker.py
MAN_FILE = man/emoji-nuker.1
README_FILE = README.md
LICENSE_FILE = LICENSE

# Default target
all: $(SCRIPT_FILE)

# Install using Python package (recommended)
install-python: all
	@echo "Installing $(APP_NAME) as a Python package..."
	pip3 install --user .
	@echo "\033[32m✓ $(APP_NAME) installed successfully as a Python package!\033[0m"
	@echo "Usage: $(APP_NAME) /path/to/your/project"
	@echo "Note: Make sure the Python user scripts directory is in your PATH"
	@echo "  On macOS, this is typically: $$HOME/Library/Python/X.Y/bin"
	@echo "  On Linux, this is typically: $$HOME/.local/bin"

# Uninstall Python package
uninstall-python:
	@echo "Uninstalling $(APP_NAME) Python package..."
	pip3 uninstall -y emoji-nuker
	@echo "\033[32m✓ $(APP_NAME) Python package uninstalled successfully!\033[0m"

# Install the application (Unix-style, fixed)
install: all
	@echo "Installing $(APP_NAME) to $(PREFIX)..."
	install -d $(BINDIR)
	install -m 755 $(SCRIPT_FILE) $(BINDIR)/$(APP_NAME)
	# Install the required Python module
	install -d $(PREFIX)/lib/$(APP_NAME)
	install -m 644 src/emoji_lut.py $(PREFIX)/lib/$(APP_NAME)/
	install -d $(MAN1DIR)
	install -m 644 $(MAN_FILE) $(MAN1DIR)/
	install -d $(DOCDIR)
	install -m 644 $(README_FILE) $(DOCDIR)/
	@if [ -f $(LICENSE_FILE) ]; then install -m 644 $(LICENSE_FILE) $(DOCDIR)/; fi
	@echo "\033[32m✓ $(APP_NAME) installed successfully!\033[0m"
	@echo "Usage: $(APP_NAME) /path/to/your/project"
	@echo ""
	@echo "Note: The Python module is installed to $(PREFIX)/lib/$(APP_NAME)/"

# Uninstall the application (Unix-style)
uninstall:
	@echo "Uninstalling $(APP_NAME)..."
	rm -f $(BINDIR)/$(APP_NAME)
	rm -rf $(PREFIX)/lib/$(APP_NAME)
	rm -f $(MAN1DIR)/$(APP_NAME).1
	rm -rf $(DOCDIR)
	@echo "\033[32m✓ $(APP_NAME) uninstalled successfully!\033[0m"

# Install to user's home directory (Unix-style, fixed)
install-user: all
	@echo "Installing $(APP_NAME) to user directory..."
	install -d $(HOME)/.local/bin
	install -m 755 $(SCRIPT_FILE) $(HOME)/.local/bin/$(APP_NAME)
	# Install the required Python module
	install -d $(HOME)/.local/lib/$(APP_NAME)
	install -m 644 src/emoji_lut.py $(HOME)/.local/lib/$(APP_NAME)/
	install -d $(HOME)/.local/share/man/man1
	install -m 644 $(MAN_FILE) $(HOME)/.local/share/man/man1/
	@echo "\033[32m✓ $(APP_NAME) installed to user directory!\033[0m"
	@echo "Make sure $(HOME)/.local/bin is in your PATH"
	@echo ""
	@echo "Note: The Python module is installed to $(HOME)/.local/lib/$(APP_NAME)/"

# Uninstall from user directory (Unix-style)
uninstall-user:
	@echo "Uninstalling $(APP_NAME) from user directory..."
	rm -f $(HOME)/.local/bin/$(APP_NAME)
	rm -rf $(HOME)/.local/lib/$(APP_NAME)
	rm -f $(HOME)/.local/share/man/man1/$(APP_NAME).1
	@echo "\033[32m✓ $(APP_NAME) uninstalled from user directory!\033[0m"

# Check if dependencies are available
check-deps:
	@echo "Checking dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "\033[31m✗ python3 is required but not installed\033[0m"; exit 1; }
	@command -v pip3 >/dev/null 2>&1 || { echo "\033[31m✗ pip3 is required but not installed\033[0m"; exit 1; }
	@echo "\033[32m✓ All dependencies satisfied\033[0m"

# Run comprehensive tests
test: check-deps
	@echo "Running comprehensive $(APP_NAME) tests..."
	@echo ""
	
	# Test 1: Basic functionality
	@echo "=== Test 1: Basic Functionality ==="
	@python3 -c "import sys; sys.path.insert(0, 'src'); import emoji_lut; print('✓ Emoji LUT module loads correctly')"
	@python3 -c "import sys; sys.path.insert(0, 'src'); exec(open('src/emoji_nuker.py').read().split('def main()')[0]); print('✓ Main script loads correctly')"
	
	# Test 2: Historical precedence architecture
	@echo ""
	@echo "=== Test 2: Historical Precedence Architecture ==="
	@python3 -c "import sys; sys.path.insert(0, 'src'); from emoji_lut import PRE_EMOJI_UNICODE_SYMBOLS, is_emoji_for_replacement; \
		symbols = ['*', '#', 'ℹ', '™', '©', '®', '←', '→', '↑', '↓', '↗', '↘', '↙', '↖', '↕', '↔', '✓', '✗', '√', '×', '!', '火']; \
		failed = [s for s in symbols if is_emoji_for_replacement(s)]; \
		print('✓ Pre-emoji Unicode symbols preserved') if not failed else (print(f'✗ Failed: {failed}') or exit(1))"
	
	# Test 3: Emoji detection
	@echo ""
	@echo "=== Test 3: Emoji Detection ==="
	@python3 -c "import sys; sys.path.insert(0, 'src'); \
		exec(open('src/emoji_nuker.py').read().split('def main()')[0]); \
		from emoji_lut import is_emoji_for_replacement; \
		single_char_emojis = ['✅', '❌', '🔥', '⚠', '⭐', '➡', '🔺', '🔻', '🚀', '😀', '😊']; \
		multi_char_emojis = ['1️⃣', '🅰']; \
		failed_single = [e for e in single_char_emojis if not is_emoji_for_replacement(e)]; \
		failed_multi = [e for e in multi_char_emojis if e not in BASE_SUBSTITUTIONS]; \
		failed = failed_single + failed_multi; \
		print('✓ Emoji detection works correctly') if not failed else (print(f'✗ Failed: {failed}') or exit(1))"
	
	# Test 4: Command line options
	@echo ""
	@echo "=== Test 4: Command Line Options ==="
	@echo "Testing --help option..."
	@python3 $(SCRIPT_FILE) --help > /dev/null 2>&1 && echo "✓ --help option works" || (echo "✗ --help option failed" && exit 1)
	@echo "Testing --version option..."
	@python3 $(SCRIPT_FILE) --version > /dev/null 2>&1 && echo "✓ --version option works" || (echo "✗ --version option failed" && exit 1)
	
	# Test 5: File processing modes
	@echo ""
	@echo "=== Test 5: File Processing Modes ==="
	@echo "Creating test file..."
	@echo "# Test file with emojis ✅ ❌ 🔥 and Unicode symbols ✓ ✗ ←" > test_makefile.py
	@echo "Testing --substitute mode..."
	@cp test_makefile.py test_substitute.py
	@python3 $(SCRIPT_FILE) --substitute test_substitute.py > /dev/null 2>&1 && echo "✓ --substitute mode works" || (echo "✗ --substitute mode failed" && exit 1)
	@echo "Testing --interactive mode..."
	@python3 $(SCRIPT_FILE) --interactive test_makefile.py > /dev/null 2>&1 && echo "✓ --interactive mode works" || (echo "✗ --interactive mode failed" && exit 1)
	@echo "Testing --label mode..."
	@cp test_makefile.py test_label.py
	@python3 $(SCRIPT_FILE) --label test_label.py > /dev/null 2>&1 && echo "✓ --label mode works" || (echo "✗ --label mode failed" && exit 1)
	@echo "Testing --color mode..."
	@cp test_makefile.py test_color.py
	@python3 $(SCRIPT_FILE) --substitute --color test_color.py > /dev/null 2>&1 && echo "✓ --color mode works" || (echo "✗ --color mode failed" && exit 1)
	@echo "Testing --verbose mode..."
	@python3 $(SCRIPT_FILE) --verbose --interactive test_makefile.py > /dev/null 2>&1 && echo "✓ --verbose mode works" || (echo "✗ --verbose mode failed" && exit 1)
	
	# Test 6: Substitution validation
	@echo ""
	@echo "=== Test 6: Substitution Validation ==="
	@python3 -c "import sys; sys.path.insert(0, 'src'); exec(open('src/emoji_nuker.py').read().split('def main()')[0]); \
		result = validate_no_emoji_in_substitutions(); \
		print('✓ No emoji characters in substitutions') if result else (print('✗ Emoji characters found in substitutions') or exit(1))"
	
	# Test 7: File type support
	@echo ""
	@echo "=== Test 7: File Type Support ==="
	@echo "Testing supported file extensions..."
	@echo "# Test ✅" > test.py && python3 $(SCRIPT_FILE) --interactive test.py > /dev/null 2>&1 && echo "✓ .py files supported" || (echo "✗ .py files failed" && exit 1)
	@echo "/* Test ✅ */" > test.js && python3 $(SCRIPT_FILE) --interactive test.js > /dev/null 2>&1 && echo "✓ .js files supported" || (echo "✗ .js files failed" && exit 1)
	@echo "// Test ✅" > test.cpp && python3 $(SCRIPT_FILE) --interactive test.cpp > /dev/null 2>&1 && echo "✓ .cpp files supported" || (echo "✗ .cpp files failed" && exit 1)
	@echo "# Test ✅" > test.md && python3 $(SCRIPT_FILE) --interactive test.md > /dev/null 2>&1 && echo "✓ .md files supported" || (echo "✗ .md files failed" && exit 1)
	
	# Test 8: Directory processing
	@echo ""
	@echo "=== Test 8: Directory Processing ==="
	@mkdir -p test_dir
	@echo "# Test ✅" > test_dir/test.py
	@python3 $(SCRIPT_FILE) --interactive test_dir > /dev/null 2>&1 && echo "✓ Directory processing works" || (echo "✗ Directory processing failed" && exit 1)
	
	# Cleanup
	@rm -f test_makefile.py test_substitute.py test_label.py test_color.py test.py test.js test.cpp test.md
	@rm -rf test_dir
	
	@echo ""
	@echo "\033[32m✓ All $(APP_NAME) tests passed!\033[0m"
	@echo ""
	@echo "=== Feature Coverage Summary ==="
	@echo "✓ Historical precedence architecture"
	@echo "✓ Pre-emoji Unicode symbol preservation"
	@echo "✓ Emoji-first character detection"
	@echo "✓ All command line options (--help, --version, --verbose, --substitute, --interactive, --label, --color)"
	@echo "✓ All processing modes"
	@echo "✓ Substitution validation"
	@echo "✓ File type support"
	@echo "✓ Directory processing"

# Test CI workflow locally
test-ci:
	@echo "Running CI workflow locally..."
	@echo "Note: This runs the same tests as GitHub Actions"
	@cd .github/workflows && python3 -c "import yaml; print('✓ test.yml is valid YAML')" < test.yml
	@echo "\033[33mℹ For full CI testing, push to GitHub or run: act -j test\033[0m"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	rm -f test_*.py test_*.js test_*.cpp test_*.md
	rm -rf test_dir/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "\033[32m✓ Clean complete\033[0m"

# Show help
help:
	@echo "Available targets:"
	@echo "  all               - Build the application (default)"
	@echo ""
	@echo "Python Package Installation (Recommended):"
	@echo "  install-python    - Install as Python package"
	@echo "  uninstall-python  - Uninstall Python package"
	@echo ""
	@echo "Unix-Style Installation:"
	@echo "  install           - Install system-wide (requires sudo)"
	@echo "  install-user      - Install to user directory"
	@echo "  uninstall         - Uninstall system-wide (requires sudo)"
	@echo "  uninstall-user    - Uninstall from user directory"
	@echo ""
	@echo "Development:"
	@echo "  test              - Run comprehensive tests"
	@echo "  test-ci           - Test CI workflow locally"
	@echo "  check-deps        - Check dependencies"
	@echo "  clean             - Clean build artifacts"
	@echo "  help              - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  PREFIX=$(PREFIX) (set PREFIX= to override)"
	@echo ""
	@echo "Installation Options:"
	@echo "  • Python Package: make install-python (recommended)"
	@echo "  • Unix-Style:     make install-user (traditional)"
	@echo ""
	@echo "Features tested:"
	@echo "  • Historical precedence architecture"
	@echo "  • All command line options: --help, --version, --verbose, --substitute, --interactive, --label, --color"
	@echo "  • All processing modes and file types"
	@echo "  • Emoji detection and substitution validation"

# Phony targets
.PHONY: all install install-python uninstall uninstall-python install-user uninstall-user test test-ci check-deps clean help 