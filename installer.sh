#!/bin/bash

# Configuration
SCRIPT_NAME="emoji-nuker"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_PATH="$INSTALL_DIR/$SCRIPT_NAME"
PYTHON_SCRIPT_CONTENT='
import os
import re
from pathlib import Path

CODE_EXTENSIONS = {".py", ".js", ".ts", ".cpp", ".c", ".h", ".java", ".rb", ".go", ".rs", ".html", ".css", ".json", ".yml", ".yaml", ".sh", ".md", ".txt"}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002700-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U00002600-\U000026FF"
    "\U0001FA70-\U0001FAFF"
    "\U000025A0-\U000025FF"
    "]+", flags=re.UNICODE,
)

def remove_emojis_from_file(file_path: Path):
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        new_content = EMOJI_PATTERN.sub("", content)
        if content != new_content:
            with file_path.open("w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Cleaned: {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def clean_directory(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in CODE_EXTENSIONS:
            remove_emojis_from_file(path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Remove emojis from code files in a project directory.")
    parser.add_argument("directory", type=str, help="Path to the root of the project directory.")
    args = parser.parse_args()

    root_path = Path(args.directory)
    if not root_path.exists() or not root_path.is_dir():
        print(f"Invalid directory: {root_path}")
    else:
        clean_directory(root_path)
'

# Ensure install directory exists
mkdir -p "$INSTALL_DIR"

#  Now write the script to disk with shebang
echo '#!/usr/bin/env python3' > "$SCRIPT_PATH"
echo "$PYTHON_SCRIPT_CONTENT" >> "$SCRIPT_PATH"
chmod +x "$SCRIPT_PATH"
echo -e "\033[32m Installed emoji-nuker to $SCRIPT_PATH\033[0m"

# Detect shell and shell config file
CURRENT_SHELL=$(basename "$SHELL")
case "$CURRENT_SHELL" in
  zsh)  SHELL_RC="$HOME/.zshrc" ;;
  bash) SHELL_RC="$HOME/.bashrc" ;;
  fish) SHELL_RC="$HOME/.config/fish/config.fish" ;;
  *)    SHELL_RC="$HOME/.profile" ;;
esac

EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'
FISH_LINE='set -gx PATH $HOME/.local/bin $PATH'

# Add export if not present
if [[ "$CURRENT_SHELL" == "fish" ]]; then
  if ! grep -Fxq "$FISH_LINE" "$SHELL_RC"; then
    echo "$FISH_LINE" >> "$SHELL_RC"
    echo -e "\033[32m Added emoji-nuker to your fish PATH in $SHELL_RC\033[0m"
  fi
else
  if ! grep -Fxq "$EXPORT_LINE" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# Added by emoji-nuker installer" >> "$SHELL_RC"
    echo "$EXPORT_LINE" >> "$SHELL_RC"
    echo -e "\033[32m Added emoji-nuker to your PATH in $SHELL_RC\033[0m"
  fi
fi

echo "Please run 'source $SHELL_RC' or restart your shell to use 'emoji-nuker'.\033[0m"
echo "Usage: emoji-nuker /path/to/your/project\033[0m"

