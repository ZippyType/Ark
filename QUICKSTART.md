# Quick Start Guide - Ark Executable & Shell

## Installation on Ubuntu

### Option 1: Quick Install (Recommended)

```bash
cd /path/to/Ark
bash install.sh
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### Option 2: Manual Install

```bash
cd /path/to/Ark
chmod +x ark
sudo ln -s $(pwd)/ark /usr/local/bin/ark
```

Or for user-only installation:
```bash
mkdir -p ~/.local/bin
ln -s $(pwd)/ark ~/.local/bin/ark
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc
```

---

## Using the Ark Shell

### Interactive Shell

Start the interactive shell:
```bash
ark
```

You'll see:
```
╔═══════════════════════════════════════════════════════════╗
║                   A R K   S H E L L                       ║
║              Version 0.1.0 - The Heart Phase              ║
║                                                           ║
║  Type: help() for help, exit() to quit                  ║
║  Use: () for code blocks, fn for functions              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

ark>
```

#### Commands in Interactive Mode

**Get Help:**
```
ark> help()
```

**Exit the Shell:**
```
ark> exit()
```

**Try Code:**
```
ark> let x = 42
ark> print(x)
```

### Running Scripts

Execute a `.ark` file directly:
```bash
ark examples/hello.ark
ark examples/calculator.ark
ark my_script.ark
```

### Running Scripts as Executables

Make a script executable and run directly:

```bash
chmod +x my_script.ark
./my_script.ark
```

This requires the shebang line at the top:
```ark
#!/usr/bin/env ark

fn main() (
    print("Hello!")
)

main()
```

---

## Shell Features

### Syntax Highlighting (via Readline)
The shell uses Python's readline module for:
- Command history (arrow up/down)
- Command editing (Ctrl+A, Ctrl+E, etc.)
- Tab completion (when available)

### Multi-line Input
The shell automatically detects incomplete code:
```
ark> fn greet(name) (
... print("Hello " + name)
... )
```

Just keep typing and press Enter. The shell will continue with `...` prompt until code is complete.

### Error Handling
Errors are caught and displayed:
```
ark> print(undefined_var)
Error: NameError: undefined_var not found
```

---

## Examples

### Example 1: Hello World
```bash
$ ark examples/hello.ark
Hello, World!
Welcome to the Ark Programming Language!
```

### Example 2: Interactive Math
```
ark> let a = 10
ark> let b = 5
ark> print(a + b)
15
```

### Example 3: Function Definition
```
ark> fn square(x) (return x * x)
ark> print(square(5))
25
```

### Example 4: Control Flow
```
ark> let x = 15
ark> if (x > 10) (print("x is big")) else (print("x is small"))
x is big
```

---

## Troubleshooting

### Issue: "ark: command not found"

**Solution 1:** Run from the Ark directory
```bash
cd /path/to/Ark
./ark
```

**Solution 2:** Reload your shell after installation
```bash
source ~/.bashrc
source ~/.zshrc
```

**Solution 3:** Check if ~/.local/bin is in PATH
```bash
echo $PATH
# Should contain: /home/username/.local/bin
```

### Issue: Permission Denied

Make the script executable:
```bash
chmod +x /path/to/Ark/ark
```

### Issue: "ModuleNotFoundError: No module named 'lexer'"

Ensure you're running from the Ark directory or that the path is correct. The script should auto-detect the module path.

### Issue: Script Execution Fails

Verify the file has the `.ark` extension:
```bash
ark my_script.ark  # ✓ Works
ark my_script.py   # ✗ Won't work
```

---

## Advanced Usage

### Passing Arguments (Future Feature)
Currently not implemented, but planned:
```bash
ark script.ark arg1 arg2
# Would be available in script as: ARGV or sys.args
```

### Importing Modules (Future Feature)
Planned for Batch 12:
```ark
import math
import utils
```

### Running in Background
```bash
ark my_script.ark &
```

---

## Performance Notes

- **Interactive Mode:** Instant startup (Python interpreter startup time ~100-300ms)
- **Script Execution:** Fast for most scripts, limited only by interpreter speed
- **Memory:** Minimal overhead (~10-20MB base)

---

## Next Steps

Once you have `ark` installed and working:

1. **Learn the Syntax:**
   ```bash
   ark examples/hello.ark
   ark examples/variables.ark
   ```

2. **Try the Interactive Shell:**
   ```bash
   ark
   ark> let message = "Hello, Ark!"
   ark> print(message)
   ```

3. **Create Your Own Script:**
   ```bash
   cat > my_first_script.ark << 'EOF'
   fn greet(name) (
       print("Welcome, " + name + "!")
   )
   
   greet("Alice")
   EOF
   
   ark my_first_script.ark
   ```

---

**Happy coding with Ark!** 🚀

For more information, check:
- `/workspaces/Ark/ARK_FORMAT.md` - File format specification
- `/workspaces/Ark/INTEGRATION.md` - IDE/editor integration
- `/workspaces/Ark/examples/README.md` - More examples
