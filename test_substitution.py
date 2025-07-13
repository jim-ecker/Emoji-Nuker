# Test file with various emojis to demonstrate substitution
print("Hello World! ↑")  # Should become "Hello World! ↑"

# Success indicators
status = "[emoji:U+2713] All tests passed"  # Should become "[emoji:U+2713] All tests passed"
error = "[emoji:U+2717] Permission denied"  # Should become "[emoji:U+2717] Permission denied"
warning = "[emoji:U+26A0] Binary file detected"  # Should become "[emoji:U+26A0] Binary file detected"

# Arrows and navigation
print("→ Next step")  # Should become "→ Next step"
print("⬅[emoji:U+FE0F] Previous step")  # Should become "← Previous step"
print("⬆[emoji:U+FE0F] Go up")  # Should become "↑ Go up"
print("⬇[emoji:U+FE0F] Go down")  # Should become "↓ Go down"

# Programming symbols
print("[emoji:U+1F40D] Python code")  # Should stay as "[emoji:U+1F40D] Python code"
print("[emoji:U+1F4BB] Computer work")  # Should stay as "[emoji:U+1F4BB] Computer work"
print("[emoji:U+1F527] Fix the bug")  # Should stay as "[emoji:U+1F527] Fix the bug"
print("[emoji:U+26A1] Fast execution")  # Should stay as "[emoji:U+26A1] Fast execution"

# Numbers and letters
print("1[emoji:U+FE0F]⃣ First item")  # Should become "1 First item"
print("2[emoji:U+FE0F]⃣ Second item")  # Should become "2 Second item"
print("🅰[emoji:U+FE0F] Option A")  # Should become "A Option A"
print("🅱[emoji:U+FE0F] Option B")  # Should become "B Option B"

# Emotions (should stay as is)
print("[emoji:U+1F605] That was close!")
print("[emoji:U+1F60A] Nice work!")
print("[emoji:U+1F914] Let me think...")

# Objects
print("[emoji:U+1F4DD] Take notes")  # Should stay as "[emoji:U+1F4DD] Take notes"
print("[emoji:U+1F4C4] Read the file")  # Should stay as "[emoji:U+1F4C4] Read the file"
print("[emoji:U+1F4C2] Open folder")  # Should stay as "[emoji:U+1F4C2] Open folder" 