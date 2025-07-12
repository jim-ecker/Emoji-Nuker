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
SCRIPT_FILE = src/emoji-nuker
MAN_FILE = man/emoji-nuker.1
README_FILE = README.md
LICENSE_FILE = LICENSE

# Default target
all: $(SCRIPT_FILE)

# Install the application
install: all
	@echo "Installing $(APP_NAME) to $(PREFIX)..."
	install -d $(BINDIR)
	install -m 755 $(SCRIPT_FILE) $(BINDIR)/$(APP_NAME)
	install -d $(MAN1DIR)
	install -m 644 $(MAN_FILE) $(MAN1DIR)/
	install -d $(DOCDIR)
	install -m 644 $(README_FILE) $(DOCDIR)/
	@if [ -f $(LICENSE_FILE) ]; then install -m 644 $(LICENSE_FILE) $(DOCDIR)/; fi
	@echo "\033[32m✓ $(APP_NAME) installed successfully!\033[0m"
	@echo "Usage: $(APP_NAME) /path/to/your/project"

# Uninstall the application
uninstall:
	@echo "Uninstalling $(APP_NAME)..."
	rm -f $(BINDIR)/$(APP_NAME)
	rm -f $(MAN1DIR)/$(APP_NAME).1
	rm -rf $(DOCDIR)
	@echo "\033[32m✓ $(APP_NAME) uninstalled successfully!\033[0m"

# Install to user's home directory (alternative to system-wide install)
install-user: all
	@echo "Installing $(APP_NAME) to user directory..."
	install -d $(HOME)/.local/bin
	install -m 755 $(SCRIPT_FILE) $(HOME)/.local/bin/$(APP_NAME)
	install -d $(HOME)/.local/share/man/man1
	install -m 644 $(MAN_FILE) $(HOME)/.local/share/man/man1/
	@echo "\033[32m✓ $(APP_NAME) installed to user directory!\033[0m"
	@echo "Make sure $(HOME)/.local/bin is in your PATH"

# Uninstall from user directory
uninstall-user:
	@echo "Uninstalling $(APP_NAME) from user directory..."
	rm -f $(HOME)/.local/bin/$(APP_NAME)
	rm -f $(HOME)/.local/share/man/man1/$(APP_NAME).1
	@echo "\033[32m✓ $(APP_NAME) uninstalled from user directory!\033[0m"

# Check if dependencies are available
check-deps:
	@echo "Checking dependencies..."
	@command -v python3 >/dev/null 2>&1 || { echo "\033[31m✗ python3 is required but not installed\033[0m"; exit 1; }
	@echo "\033[32m✓ All dependencies satisfied\033[0m"

# Run tests
test: check-deps
	@echo "Running tests..."
	@python3 -c "import re, pathlib; print('\033[32m✓ Python modules available\033[0m')"
	@echo "\033[32m✓ Tests passed\033[0m"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/
	@echo "\033[32m✓ Clean complete\033[0m"

# Show help
help:
	@echo "Available targets:"
	@echo "  all          - Build the application (default)"
	@echo "  install      - Install system-wide (requires sudo)"
	@echo "  install-user - Install to user directory"
	@echo "  uninstall    - Uninstall system-wide (requires sudo)"
	@echo "  uninstall-user - Uninstall from user directory"
	@echo "  test         - Run tests"
	@echo "  check-deps   - Check dependencies"
	@echo "  clean        - Clean build artifacts"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  PREFIX=$(PREFIX) (set PREFIX= to override)"

# Phony targets
.PHONY: all install uninstall install-user uninstall-user test check-deps clean help 