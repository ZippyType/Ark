# Ark Programming Language

A high-level, simple-to-use language with a Python-based core. Uses `()` for all block scoping.

## Installation

```bash
bash install.sh
```

## Quick Start

```bash
# Run a file
ark hello.ark

# Interactive shell
ark

# Run code from command line
ark -c 'print("Hello")'
```

## Syntax

### Variables
```
x = 10
name = "Ark"
is_active = true
```

### Functions
```
fn add(a, b) (
    return a + b
)

result = add(5, 10)
```

### Control Flow
```
if (condition) (
    print("yes")
) else (
    print("no")
)

while (x > 0) (
    print(x)
    x = x - 1
)

for i in [1, 2, 3] print(i)
```

### Data Structures
```
numbers = [1, 2, 3]
person = {"name": "Alice"}

print(numbers[0])
print(person["name"])
```

### Import
```
import("module.ark")
```

### Error Handling
```
try (
    x = 10 / 0
) catch (e) (
    print("Error: ")
    print(e)
)
```

---

## Batch Checklist

Phase 1: Core Compiler Pipeline
- [x] Batch 1: Advanced Lexer - Tokenizing `()`, strings, numbers, keywords
- [x] Batch 2: AST Node Definitions - Tree structure for nested blocks
- [x] Batch 3: Recursive Descent Parser - Tokens to AST
- [x] Batch 4: Interpreter Engine - Visitor pattern execution
- [x] Batch 5: Memory & Variables - Scoped variable storage
- [x] Batch 6: Math & Comparison - Full PEMDAS, `**` exponent, boolean logic

Phase 2: Advanced Data & Logic
- [x] Batch 7: Control Flow (Part 1) - Implementation of if, else, elif
- [x] Batch 8: Control Flow (Part 2) - Implementation of while and for loops
- [x] Batch 9: Native Data Structures - Lists [] and Dicts {} support
- [x] Batch 10: Error Handling - try() catch() system

Phase 3: System, Modules & Files
- [x] Batch 11: Functions & Scope - Parameters, return values, recursion
- [x] Batch 12: The Import System - Importing other .ark files

- [x] Batch 13: File System API - open, write, read, delete
- [x] Batch 14: System Shell - sys.run() command

Phase 4: GUI & Desktop Apps
- [ ] Batch 15: GUI Core - Tkinter integration
- [ ] Batch 16: UI Elements - Windows, Buttons, Inputs, Labels
- [ ] Batch 17: Styles & Layouts - Padding, colors, grid
- [ ] Batch 18: Event Binding - GUI triggers

Phase 5: Internet, Web & Packaging
- [ ] Batch 19: Network Engine - HTTP library support
- [ ] Batch 20: HTML/CSS Renderer - Web-styled content
- [ ] Batch 21: Binary Builder - PyInstaller for .exe/.appimage

---

**Current Status**: Batch 14 complete!

---

## Examples

See `/workspaces/Ark/examples/` for sample Ark programs.

## License

GPL 3.0