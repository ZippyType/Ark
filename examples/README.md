# Ark Examples

This directory contains example Ark programs demonstrating the language's syntax and features.

## Available Examples

### 1. **hello.ark** - Hello World
**What it teaches:** Basic print statements and function definitions
- Simple `fn main()` function
- Basic `print()` usage
- Comment syntax (`//`)

**Run:** `ark hello.ark`

---

### 2. **variables.ark** - Variables and Operations
**What it teaches:** Variable declaration, arithmetic, and basic types
- Variable declaration with `let`
- String and number literals
- Arithmetic operations (`+`, `-`, `*`)
- Boolean values (`true`, `false`)
- String concatenation

**Run:** `ark variables.ark`

---

### 3. **functions.ark** - Functions and Parameters
**What it teaches:** Function definitions, parameters, return values, and conditionals
- Function definitions with `fn name(params) (...)`
- Parameter passing
- Return statements
- `if/else` conditionals
- String interpolation with `+`

**Run:** `ark functions.ark`

---

### 4. **loops.ark** - Loops and Recursion
**What it teaches:** While loops, for loops, and recursive functions
- `while` loops with conditions
- `for` loops with ranges (future: `range()` function)
- Recursion (factorial example)
- Loop counters and accumulators

**Run:** `ark loops.ark`

---

### 5. **calculator.ark** - Advanced Example
**What it teaches:** Multiple functions, complex control flow, and practical patterns
- Multiple function definitions
- String-based operation dispatch
- Nil handling
- `elif` conditionals
- Recursive algorithms (Fibonacci)
- Error handling for division by zero

**Run:** `ark calculator.ark`

---

## Syntax Cheat Sheet

### Variables
```ark
let name = "value"
let x = 42
let is_true = true
```

### Functions
```ark
fn name(param1, param2) (
    // code here
    return result
)

name(arg1, arg2)  // function call
```

### Conditionals
```ark
if (condition) (
    // code if true
) else (
    // code if false
)

if (x > 10) (
    // ...
) elif (x > 5) (
    // ...
) else (
    // ...
)
```

### Loops
```ark
while (condition) (
    // code
)

for (i in range(0, 10)) (
    // code
)
```

### Operators
- **Arithmetic:** `+`, `-`, `*`, `/`, `%`, `**`
- **Comparison:** `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Logical:** `and`, `or`, `not`

### Built-in Functions
- `print(value)` - Print to console
- `type(value)` - Get type of value
- `range(start, end)` - Create a range (future)

## Learning Path

1. Start with **hello.ark** for basic syntax
2. Move to **variables.ark** to understand data types
3. Explore **functions.ark** for reusable code
4. Practice **loops.ark** for iteration patterns
5. Study **calculator.ark** for complex logic

Happy coding in Ark! 🚀
