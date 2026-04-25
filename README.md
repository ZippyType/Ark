# 🏹 Ark Programming Language

A simple, high-performance language with a Python-based core. **Ark uses `()` for all block scoping** (functions, loops, conditionals) to maintain a clean, parenthetical aesthetic.

```ark
fn greet(name) (
    print("Hello, " + name + "!")
)

greet("World")
```

---

## Features

✨ **Simple Syntax** - Parentheses `()` for all code blocks  
🚀 **Fast** - Python 3.12+ interpreter  
📚 **Easy to Learn** - Python-like semantics with Lisp-style syntax  
🎯 **Cross-Platform** - Runs on Linux, macOS, Windows  
📦 **Batteries Included** - File I/O, networking, GUI (future)  

---

## Quick Start

### Installation (Ubuntu/Linux)

```bash
git clone https://github.com/ZippyType/Ark.git
cd Ark
bash install.sh
source ~/.bashrc
```

### Interactive Shell

```bash
ark
```

```
ark> let x = 42
ark> print(x)
42
ark> exit()
```

### Run a Script

```bash
ark examples/hello.ark
```

### Make Scripts Executable

```bash
chmod +x my_script.ark
./my_script.ark  # Requires shebang: #!/usr/bin/env ark
```

---

## Syntax Overview

### Variables
```ark
let name = "Alice"
let age = 30
let active = true
```

### Functions
```ark
fn add(a, b) (
    return a + b
)

print(add(5, 3))  // Output: 8
```

### Conditionals
```ark
if (x > 10) (
    print("Big")
) elif (x > 5) (
    print("Medium")
) else (
    print("Small")
)
```

### Loops
```ark
while (x > 0) (
    print(x)
    x = x - 1
)

for (i in range(0, 10)) (
    print(i)
)
```

### Print & Type
```ark
print("Hello, " + "World!")
print(type(42))  // "number"
```

---

## Examples

Browse the [examples/](examples/) directory for complete programs:

- **hello.ark** - Hello World
- **variables.ark** - Data types and operations
- **functions.ark** - Function definitions and calls
- **loops.ark** - Loops and recursion
- **calculator.ark** - Advanced control flow

Run any example:
```bash
ark examples/calculator.ark
```

---

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Getting started with the executable and shell
- **[ARK_FORMAT.md](ARK_FORMAT.md)** - File format specification
- **[INTEGRATION.md](INTEGRATION.md)** - IDE/editor integration
- **[ROADMAP.md](#roadmap)** - Development roadmap

---

## Roadmap

### Phase 1: The Core Compiler Pipeline ✅ IN PROGRESS
- **Batch 1:** Advanced Lexer ✅
- **Batch 2:** AST Node Definitions (next)
- **Batch 3:** Recursive Descent Parser
- **Batch 4:** The Interpreter Engine
- **Batch 5:** Memory & Variables

### Phase 2: Advanced Data & Logic
- **Batch 6:** Math & Comparison
- **Batch 7:** Control Flow (if/else)
- **Batch 8:** Control Flow (loops)
- **Batch 9:** Native Data Structures (lists, dicts)
- **Batch 10:** Error Handling (try/catch)

### Phase 3: System, Modules & Files
- **Batch 11:** Functions & Scope
- **Batch 12:** The Import System
- **Batch 13:** File System API
- **Batch 14:** System Shell Integration

### Phase 4: GUI & Desktop Apps
- **Batch 15:** GUI Core (Tkinter/CustomTkinter)
- **Batch 16:** UI Elements
- **Batch 17:** Styles & Layouts
- **Batch 18:** Event Binding

### Phase 5: Internet, Web & Packaging
- **Batch 19:** Network Engine (HTTP, JSON)
- **Batch 20:** HTML/CSS Renderer
- **Batch 21:** Binary Builder (PyInstaller integration)

---

## Command-Line Usage

### Run Interactive Shell
```bash
ark
```

### Run a Script
```bash
ark script.ark
```

### Check Version
```bash
ark --version
# or
ark -v
```

### Get Help
```bash
ark help
# or
ark -h
```

### Within the Shell

```
ark> help()       # Show help
ark> exit()       # Exit shell
```

---

## Technical Details

**Language:** Python 3.12+  
**Architecture:** Lexer → Parser → AST → Interpreter  
**License:** [LICENSE](LICENSE)  

---

## Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon)

---

## License

Ark is licensed under the [license](LICENSE) file in this repository.

---

**Made with ❤️ for simplicity and performance**
