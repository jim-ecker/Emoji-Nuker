#!/bin/bash

# Configuration
SCRIPT_NAME="emoji-nuker"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
SHELL_RC="$HOME/.zshrc"
EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'
INSTALL_COMMENT="# Added by emoji-nuker installer"

echo "🔧 Uninstalling $SCRIPT_NAME..."

# Step 1: Remove the installed script
if [ -f "$SCRIPT_PATH" ]; then
    rm "$SCRIPT_PATH"
    echo "🗑️  Removed: $SCRIPT_PATH"
else
    echo "⚠️  No installed script found at $SCRIPT_PATH"
fi

# Step 2: Remove the export line and comment from .zshrc
if grep -Fxq "$INSTALL_COMMENT" "$SHELL_RC"; then
    tmpfile=$(mktemp)
    awk -v comment="$INSTALL_COMMENT" -v export_line="$EXPORT_LINE" '
    $0 == comment { skip = 1; next }
    $0 == export_line && skip == 1 { skip = 0; next }
    { print }
    ' "$SHELL_RC" > "$tmpfile"
    mv "$tmpfile" "$SHELL_RC"
    echo "🧹 Cleaned PATH export from $SHELL_RC"
else
    echo "ℹ️  No PATH export inserted by this installer found in $SHELL_RC"
fi

echo "✅ Uninstall complete. Run 'source $SHELL_RC' or restart your shell."


