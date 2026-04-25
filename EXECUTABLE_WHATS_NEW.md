# Ark Executable - What's New

## Summary

You now have a complete **executable and interactive shell** for the Ark programming language!

---

## Files Created/Updated

### Core Executable
| File | Purpose |
|------|---------|
| **`ark`** | Main executable - run `ark` for shell or `ark script.ark` for files |
| **`install.sh`** | Installation script for Ubuntu/Linux - automatically sets up PATH |

### Documentation
| File | Purpose |
|------|---------|
| **`EXECUTABLE_SETUP.md`** | How to install and use the executable (this guide) |
| **`QUICKSTART.md`** | Quick reference for the shell and file execution |
| **`README.md`** | Updated project overview (now super comprehensive!) |
| **`ARK_FORMAT.md`** | File format specification (already created) |
| **`INTEGRATION.md`** | IDE/editor integration (already created) |

### Examples
Examples from the previous batch (still available):
- `examples/hello.ark`
- `examples/variables.ark`
- `examples/functions.ark`
- `examples/loops.ark`
- `examples/calculator.ark`
- `examples/README.md`

---

## Quick Setup & Test

### 1. Make Executable
```bash
cd /workspaces/Ark
chmod +x ark
```

### 2. Option A: Easy Install (Recommended)
```bash
bash install.sh
source ~/.bashrc
ark --version
```

### 2. Option B: Manual Setup
```bash
mkdir -p ~/.local/bin
ln -s $(pwd)/ark ~/.local/bin/ark
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Test It!
```bash
# Test 1: Interactive shell
ark

# Test 2: Run a script
ark examples/hello.ark

# Test 3: Check version
ark --version

# Test 4: Exit from shell (as you requested)
ark> exit()
```

---

## What You Can Do Now

### ✅ Implemented

- **Run files:** `ark script.ark`
- **Interactive shell:** `ark` (then type code)
- **Exit shell:** `exit()` (exactly like Python)
- **Help:** `help()` in shell or `ark --help`
- **Version:** `ark --version` or `ark -v`
- **Multi-line input:** Type incomplete code and continue on next line
- **Make scripts executable:** `chmod +x script.ark && ./script.ark`

### 🔜 Coming Soon (Batches 2-4)

Once the parser and interpreter are built, you'll be able to:
- Actually execute code (currently just tokenizes)
- Store and retrieve variables
- Call functions
- Use control flow
- See real program output

---

## How It Works Right Now

**The Lexer Phase (Batch 1):**
```
Your Code → Lexer → Tokens → Display
```

You type:
```
ark> print("Hello")
```

The shell shows:
```
[Tokens: 2 total]
  IDENTIFIER: print
  STRING: Hello
```

This proves your syntax is recognized! Once the interpreter is built (Batch 4), it will execute:
```
ark> print("Hello")
Hello
```

---

## File Descriptions

### `ark` (The Main Executable)
- Written in Python
- Always looks for the `lexer.py` from Batch 1
- Supports two modes:
  1. **Interactive mode** (no arguments) - starts REPL shell
  2. **File mode** (with filename argument) - executes `.ark` file
- 200+ lines of well-documented Python
- Features: help, version info, error handling, multi-line support

### `install.sh` (Installation Helper)
- Bash script that:
  1. Makes `ark` executable
  2. Creates symlink to `/usr/local/bin/` (system-wide) OR `~/.local/bin/` (user-only)
  3. Updates `~/.bashrc` and `~/.zshrc` if needed
  4. Verifies the installation
  5. Provides instructions for next steps
- Safe - checks for existing files and permissions
- Works on Ubuntu, Debian, and most Linux distros

---

## Shell Interface

The interactive shell provides:

```
╔═══════════════════════════════════════════════════════════╗
║                   A R K   S H E L L                       ║
║              Version 0.1.0 - The Heart Phase              ║
║                                                           ║
║  Type: help() for help, exit() to quit                  ║
║  Use: () for code blocks, fn for functions              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

ark> _
```

### Prompt Modes
- `ark> ` - Ready for new command
- `... ` - Continuing multi-line code

### Special Commands
- `help()` - Show help
- `exit()` - Quit shell (as requested!)
- `Ctrl+C` - Cancel current input
- `Ctrl+D` - Alternative exit
- Arrow keys - Command history (via readline)

---

## Next Steps

1. **Install:** Follow setup section above
2. **Test:** Try the examples and interactive shell
3. **Read:** Check out `QUICKSTART.md` for more examples
4. **Create:** Write your first `.ark` script
5. **Wait:** I'll provide Batch 2 (AST Node Definitions) when you say "Next Batch"

---

## Q&A

**Q: How do I use `exit()`?**  
A: Type `exit()` in the shell and press Enter. It's exactly like Python!

**Q: Can I run scripts with arguments?**  
A: Not yet - this is planned for later batches.

**Q: What if I want to use a different shell prompt?**  
A: Edit the `ark` file and change line ~90 from `prompt = "ark> "` to whatever you want.

**Q: Will the executable work on macOS/Windows?**  
A: The Python script will, but installation steps differ. Use Python directly on those platforms for now.

**Q: How do I uninstall?**  
A: Remove the symlink:
```bash
sudo rm /usr/local/bin/ark
# or
rm ~/.local/bin/ark
```

---

## Architecture Overview

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ ark shell │ ← You are here (works!)
    └────┬─────┘
         │
    ┌────▼─────────┐
    │  Lexer.py    │ ← Batch 1 (complete)
    └────┬─────────┘
         │
    ┌────▼──────────┐
    │  Parser.py    │ ← Batch 2 (next)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  Interp.py    │ ← Batch 4 (later)
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  Output       │
    └───────────────┘
```

You have the top two layers ready. Batches 2-4 will complete the pipeline!

---

**Ready to code!** 🚀

For more details, see:
- [EXECUTABLE_SETUP.md](EXECUTABLE_SETUP.md) - This file
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [README.md](README.md) - Full project overview
