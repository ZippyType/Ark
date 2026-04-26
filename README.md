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
if (x > 10) (
    print("greater")
) else (
    print("less")
)

while (x > 0) (
    print(x)
    x = x - 1
)
```

### Data Structures
```
numbers = [1, 2, 3, 4, 5]
person = {"name": "Alice", "age": 25}

print(numbers[0])
print(person["name"])
```

### Built-in Functions
```
print(value)     # Print to stdout
type(value)      # Get type name
len(value)      # Get length
str(value)      # Convert to string
int(value)      # Convert to integer
float(value)    # Convert to float
bool(value)      # Convert to boolean
list(value)     # Convert to list
dict(value)     # Convert to dict
input(prompt)  # Get user input
range(n)        # Create range
abs(n)          # Absolute value
min(a, b)       # Minimum
max(a, b)       # Maximum
sum(list)       # Sum of list
sorted(list)    # Sorted list
```

## File Extension

Use `.ark` for Ark source files.

## License

GPL 3.0