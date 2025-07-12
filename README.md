# Emoji Nuker

**Emoji Nuker** is a lightweight utility that scans your project directory and removes all emojis from code files. It’s especially useful for cleaning up emoji-laden comments, log messages, or commit artifacts in codebases before production or archiving.

---

## ✨ Features

- Recursively scans your project directory
- Removes emojis from common source code files:
  - `.py`, `.js`, `.ts`, `.cpp`, `.c`, `.h`, `.java`, `.go`, `.rs`, `.html`, `.css`, `.json`, `.yml`, `.yaml`, etc.
- Simple one-line install
- Shell command usage: `emoji-nuker /path/to/project`
- Includes clean uninstall script

---

## 📦 Installation

Run the install script to set up `emoji-nuker` in your shell:

```bash
./install_emoji_nuker.sh
```

This installs the tool to `~/.local/bin/emoji-nuker` and adds it to your `PATH` via `~/.zshrc` if needed.

---

## 🚀 Usage

```bash
emoji-nuker /path/to/your/project
```

It will recursively find all matching code files and strip out any emojis.

---

## 🧼 Uninstallation

To fully remove Emoji Nuker from your system:

```bash
./uninstall_emoji_nuker.sh
```

This will:
- Delete the `emoji-nuker` script from `~/.local/bin`
- Remove the `PATH` export line from your `~/.zshrc` (if it was added by the installer)

---

## 🔧 Customization

You can modify the file extensions and emoji matching rules in the `install_emoji_nuker.sh` script. By default, it targets the most common programming and markup formats.

---

## 🛡️ License

MIT License – use freely, modify wildly, share generously.

---

## 💡 Why Emoji Nuker?

Because not every production system wants to parse 🐍, 🚀, or 😅.
