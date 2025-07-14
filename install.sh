#!/bin/bash
#
# Emoji Nuker Installation Script
# ===============================
#
# This script installs emoji-nuker as a Python package and sets up the PATH
# automatically for the current user.
#

set -e

echo "🚀 Installing Emoji Nuker..."
echo ""

# Check if required commands exist
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is required but not installed."
    echo "Please install Python 3.6 or later and try again."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

# Install the package
echo "📦 Installing emoji-nuker Python package..."
pip3 install --user .

# Detect the Python user scripts directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    USER_SCRIPTS_DIR="$HOME/Library/Python/$PYTHON_VERSION/bin"
else
    # Linux and others
    USER_SCRIPTS_DIR="$HOME/.local/bin"
fi

echo ""
echo "✅ Installation completed successfully!"
echo ""

# Check if the scripts directory is in PATH
if [[ ":$PATH:" == *":$USER_SCRIPTS_DIR:"* ]]; then
    echo "✅ PATH is already configured correctly."
    echo "You can now run: emoji-nuker --help"
else
    echo "⚠️  The Python user scripts directory is not in your PATH."
    echo "   Scripts directory: $USER_SCRIPTS_DIR"
    echo ""
    echo "To use emoji-nuker from anywhere, add this line to your shell profile:"
    echo ""
    
    if [[ "$SHELL" == *"zsh"* ]]; then
        PROFILE_FILE="~/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        PROFILE_FILE="~/.bashrc"
    else
        PROFILE_FILE="~/.profile"
    fi
    
    echo "   echo 'export PATH=\"\$PATH:$USER_SCRIPTS_DIR\"' >> $PROFILE_FILE"
    echo ""
    echo "Then restart your terminal or run:"
    echo "   source $PROFILE_FILE"
    echo ""
    echo "Alternatively, you can run emoji-nuker with the full path:"
    echo "   $USER_SCRIPTS_DIR/emoji-nuker --help"
fi

echo ""
echo "📚 Usage examples:"
echo "   emoji-nuker /path/to/project           # Remove emojis from directory"
echo "   emoji-nuker --substitute /path         # Replace with Unicode alternatives"
echo "   emoji-nuker --interactive /path        # Preview changes without modifying"
echo "   emoji-nuker --help                     # Show all options"
echo ""
echo "Happy emoji nuking! 🎯" 