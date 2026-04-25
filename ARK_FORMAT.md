# Ark Language File Format Specification

## File Extension
- **Primary:** `.ark`
- **MIME Type:** `text/x-ark` (application/x-ark for executable)

## File Structure

### Header (Optional)
Ark files may start with a shebang line for executable scripts:
```
#!/usr/bin/env ark
```

### Encoding
- **Default:** UTF-8
- **Supported:** Any ASCII-compatible encoding

## File Organization

### Typical Structure
```
1. Shebang (optional for scripts)
2. Comments/Documentation
3. Imports (future feature)
4. Global variable declarations (let)
5. Function definitions (fn)
6. Main execution code
```

### Example
```ark
#!/usr/bin/env ark

// documentation and comments

let GLOBAL_VAR = 100

fn function_name() (
    // code
)

// Execution starts here
function_name()
```

## Syntax Rules

### Code Blocks
All code blocks use parentheses `()`:
- Functions: `fn name() (...)`
- Conditionals: `if (condition) (...)`
- Loops: `while (condition) (...)`

### Comments
- Single-line: `//` or `#`
- No multi-line comments (keep it simple)

### Statements
- Statements can be separated by newlines or semicolons (semicolons optional)
- Each logical statement is independent

### Keywords
Reserved words that cannot be used as identifiers:
```
fn, if, else, elif, while, for, let, return, print, type,
true, false, nil, in, break, continue, and, or, not
```

## File Size & Performance
- **Recommended Max Size:** 10,000 lines (logically split larger projects)
- **No Hard Limit:** Ark can parse and interpret any size file
- **Performance:** Linear with file size

## Distribution & Packaging

### Standalone Scripts
```bash
chmod +x script.ark
./script.ark
```

### Compiled/Packaged Binaries
- `.exe` (Windows)
- `.appimage` (Linux)
- `.pkg` (macOS)
- `.apk` (Android - future)

### Module Imports (Future)
```ark
import filename
import "path/to/module"
```

## Best Practices

1. **File Naming:** Use lowercase with underscores (snake_case)
   - ✓ `my_script.ark`
   - ✓ `calculator.ark`
   - ✗ `MyScript.ark` (not conventional)

2. **Organization:** Group related functions together

3. **Documentation:** Use comments generously
   ```ark
   // Function: add(a, b)
   // Purpose: Adds two numbers
   // Args: a (number), b (number)
   // Returns: sum (number)
   fn add(a, b) (
       return a + b
   )
   ```

4. **Modularity:** Keep functions small and focused

5. **Naming Conventions:**
   - Functions: `lowercase_with_underscores`
   - Variables: `lowercase_with_underscores`
   - Constants: `UPPERCASE_WITH_UNDERSCORES` (future support)

## Security Considerations

- **No eval():** Ark does not support runtime code execution
- **Input Validation:** Handle user input carefully
- **File Access:** Restricted by OS permissions (future sys module)

---

**Ark Format Version:** 0.1.0
**Last Updated:** 2026-04-25
