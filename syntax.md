# Ark Programming Language - Syntax Reference

A complete reference for the Ark programming language syntax and built-in functions.

## Table of Contents

1. [Variables](#variables)
2. [Data Types](#data-types)
3. [Operators](#operators)
4. [Functions](#functions)
5. [Control Flow](#control-flow)
6. [Data Structures](#data-structures)
7. [Error Handling](#error-handling)
8. [File Operations](#file-operations)
9. [System Commands](#system-commands)
10. [GUI Programming](#gui-programming)
11. [Networking](#networking)
12. [Built-in Functions](#built-in-functions)

---

## Variables

```ark
x = 10
name = "Ark"
is_active = true
PI = 3.14159
```

Variables are dynamically typed. No declaration keywords needed.

---

## Data Types

| Type | Example | Description |
|------|---------|-------------|
| Integer | `42` | Whole numbers |
| Float | `3.14` | Decimal numbers |
| String | `"Hello"` | Text (use double quotes) |
| Boolean | `true` / `false` | Logical values |
| List | `[1, 2, 3]` | Ordered collections |
| Dict | `{"name": "Alice"}` | Key-value pairs |

---

## Operators

### Arithmetic
```ark
+      # Addition
-      # Subtraction
*      # Multiplication
/      # Division
%      # Modulo (remainder)
**     # Exponentiation
```

### Comparison
```ark
==     # Equal
!=     # Not equal
<      # Less than
>      # Greater than
<=     # Less than or equal
>=     # Greater than or equal
```

### Logical
```ark
and    # Logical AND
or     # Logical OR
not    # Logical NOT
```

### Unary
```ark
-x     # Negative
not x  # Boolean NOT
```

### Assignment
```ark
=      # Assignment
x += 1 # Increment (in-place)
```

### PEMDAS Order
Ark follows standard mathematical precedence:
1. Parentheses `()`
2. Exponent `**`
3. Multiplication/Division `* / %`
4. Addition/Subtraction `+ -`

---

## Functions

### Declaration
```ark
fn function_name(param1, param2) (
    return param1 + param2
)
```

### Calling
```ark
result = function_name(5, 10)
```

### Returning Values
```ark
fn greet(name) (
    return "Hello, " + name
)
```

### Higher-Order Functions
```ark
fn apply(func, value) (
    return func(value)
)

fn double(x) (
    return x * 2
)

result = apply(double, 5)
```

### Closures
```ark
fn outer(x) (
    fn inner(y) (
        return x + y
    )
    return inner
)

add5 = outer(5)
print(add5(10))
```

---

## Control Flow

### If-Else
```ark
if (x > 10) (
    print("greater")
) else (
    print("less or equal")
)
```

### If-Elif-Else
```ark
if (score >= 90) (
    print("A")
) elif (score >= 80) (
    print("B")
) elif (score >= 70) (
    print("C")
) else (
    print("F")
)
```

### While Loop
```ark
i = 0
while (i < 5) (
    print(i)
    i = i + 1
)
```

### For Loop
```ark
for item in [1, 2, 3, 4, 5] (
    print(item)
)
```

### Break and Continue
```ark
for i in [1, 2, 3, 4, 5] (
    if (i == 3) (
        break
    )
    print(i)
)
```

```ark
for i in [1, 2, 3, 4, 5] (
    if (i % 2 == 0) (
        continue
    )
    print(i)
)
```

---

## Data Structures

### Lists
```ark
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, true]

first = numbers[0]
last = numbers[len(numbers) - 1]

append(numbers, 6)
```

### List Operations
```ark
nums = [1, 2, 3, 4, 5]
nums[0] = 10
slice = nums[1:3]
length = len(nums)
```

### Dicts
```ark
person = {
    "name": "Alice",
    "age": 25,
    "city": "NYC"
}

name = person["name"]
person["email"] = "alice@example.com"
```

### Nested Structures
```ark
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[1][2])

users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
]
```

### String Indexing
```ark
text = "Hello World"
first_char = text[0]
substring = text[0:5]
```

---

## Error Handling

```ark
try (
    result = 10 / 0
) catch (e) (
    print("Error caught:")
    print(e)
)
```

### Without variable
```ark
try (
    x = dangerous_operation()
) catch (
    print("Something went wrong")
)
```

---

## File Operations

### Reading a File
```ark
content = read_file("path/to/file.txt")
print(content)
```

### Writing a File
```ark
write_file("output.txt", "Hello World!")
```

### Deleting a File
```ark
delete_file("old_file.txt")
```

### File with Lines
```ark
lines = []
append(lines, "Line 1")
append(lines, "Line 2")
content = join(lines, "\n")
write_file("data.txt", content)
```

---

## System Commands

### Running Shell Commands
```ark
result = run("echo Hello from Ark")
print(result)
```

### Running System Commands
```ark
result = run("ls -la")
print(result)

result = run("dir")
print(result)
```

---

## GUI Programming

### Creating a Window
```ark
win = window("My App", 800, 600)
```

### Adding a Label
```ark
lbl = label(win, "Welcome to Ark!")
lbl.config(font=Font("Arial", 24))
lbl.pack()
```

### Adding a Button
```ark
fn on_click() (
    print("Button clicked!")
)

btn = button(win, "Click Me", on_click)
btn.pack()
```

### Getting Input
```ark
entry = entry(win)
entry.pack()

fn submit() (
    text = entry.get()
    print(text)
)

btn = button(win, "Submit", submit)
btn.pack()
```

### Message Boxes
```ark
message("Hello!", "Greeting")
message("Error occurred!", "Error", "error")
confirmed = ask_yes_no("Continue?", "Confirm")
```

### File Dialogs
```ark
path = ask_file("Select a file")
save_path = ask_save("Save as")
folder = ask_dir("Choose folder")
```

### Canvas for Drawing
```ark
cvs = canvas(win, width=400, height=400)
cvs.pack()
cvs.create_rectangle(50, 50, 200, 200, fill=Color.RED)
cvs.create_oval(100, 100, 300, 300, fill=Color.BLUE)
```

### Layout with Pack
```ark
top = frame(win)
top.pack(side=TOP, fill=X)

label(top, "Header").pack()
button(top, "Left").pack(side=LEFT)
button(top, "Right").pack(side=RIGHT)
```

### Layout with Grid
```ark
label(win, "Name:").grid(row=0, column=0)
entry(win).grid(row=0, column=1)
label(win, "Age:").grid(row=1, column=0)
entry(win).grid(row=1, column=1)
```

### Colors
```ark
Color.RED
Color.GREEN
Color.BLUE
Color.YELLOW
Color.ORANGE
Color.PURPLE
Color.WHITE
Color.BLACK
Color.GRAY
```

### Fonts
```ark
Font("Arial", 12)
Font("Courier", 14, "bold")
Font("Times", 16, "italic")
```

### Starting the App
```ark
win.mainloop()
```

### Example: Complete App
```ark
win = window("Counter App", 300, 200)

count = 0

fn update_label() (
    lbl.config(text="Count: " + str(count))
)

fn increment() (
    global count
    count = count + 1
    update_label()
)

fn decrement() (
    global count
    count = count - 1
    update_label()
)

lbl = label(win, "Count: 0")
lbl.pack(pady=10)

button(win, "-", decrement).pack(side=LEFT, padx=10)
button(win, "+", increment).pack(side=LEFT, padx=10)

win.mainloop()
```

---

## Networking

### HTTP GET
```ark
result = http_get("https://api.example.com/data")
print(result)
```

### HTTP POST
```ark
data = "name=Alice&age=25"
result = http_post("https://api.example.com/submit", data)
print(result)
```

### Example: Fetch JSON
```ark
data = http_get("https://jsonplaceholder.typicode.com/todos/1")
print(data)
```

---

## Built-in Functions

### Print & Input
```ark
print("Hello World")
print(1, 2, 3)
name = input("Enter your name: ")
```

### Type Conversion
```ark
str(42)      # "42"
int("123")   # 123
float("3.14")# 3.14
bool(1)      # true
bool(0)      # false
list(1, 2, 3) # [1, 2, 3]
dict({"a": 1}) # {"a": 1}
```

### Type Checking
```ark
type(42)       # "int"
type("hello")  # "str"
type(true)     # "bool"
type([1, 2])   # "list"
type({"a": 1}) # "dict"
```

### Collection Functions
```ark
len([1, 2, 3])           # 3
sum([1, 2, 3, 4])        # 10
min(1, 2, 3)             # 1
max(1, 2, 3)             # 3
abs(-5)                  # 5
sorted([3, 1, 2])        # [1, 2, 3]
reversed([1, 2, 3])      # [3, 2, 1]
enumerate(["a", "b"])    # [[0, "a"], [1, "b"]]
zip([1, 2], ["a", "b"])  # [[1, "a"], [2, "b"]]
```

### Functional Programming
```ark
fn double(x) (
    return x * 2
)

fn is_even(x) (
    return x % 2 == 0
)

nums = [1, 2, 3, 4, 5]

doubled = map(double, nums)    # [2, 4, 6, 8, 10]
evens = filter(is_even, nums) # [2, 4]
```

### Range
```ark
range(5)          # [0, 1, 2, 3, 4]
range(1, 6)       # [1, 2, 3, 4, 5]
range(0, 10, 2)   # [0, 2, 4, 6, 8]
```

### String Operations
```ark
len("hello")                # 5
"hello" + " " + "world"     # "hello world"
"hello"[0]                  # "h"
"hello"[1:4]                # "ell"
```

---

## Import System

### Importing Ark Files
```ark
import("path/to/module.ark")
```

### Using Imported Functions
```ark
import("utils.ark")
result = add(5, 10)
```

---

## Examples

See the `examples/` directory for complete programs:
- `examples/getting-started/` - First steps
- `examples/builtins/` - Built-in functions
- `examples/control-flow/` - Loops and conditionals
- `examples/functions/` - Function examples
- `examples/data-structures/` - Lists and dicts
- `examples/gui/` - GUI applications
- `examples/networking/` - HTTP examples
- `examples/files/` - File operations
- `examples/math/` - Math operations

---

## Running Ark

```bash
# Run a file
ark program.ark

# Interactive shell
ark

# One-liner
ark -c 'print("Hello")'
```