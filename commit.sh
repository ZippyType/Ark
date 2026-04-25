#!/bin/bash

# Git commit script for Ark repository

cd /workspaces/Ark

echo "📦 Staging files..."
git add -A

echo "✅ Files staged. Running commit..."
git commit -m "Batch 1: Complete Lexer, Ark Executable & Simple Interpreter

Added:
- lexer.py: Advanced tokenizer for Ark syntax
- simple_interpreter.py: Basic interpreter for immediate execution
- ark: Executable shell for interactive REPL and file execution
- examples/: Test programs (hello.ark, variables.ark, functions.ark, loops.ark, calculator.ark)
- LOGO.txt: ASCII art logo with color scheme
- ARK_FORMAT.md: File format specification
- INTEGRATION.md: IDE/editor integration guide
- QUICKSTART.md: Quick start guide
- EXECUTABLE_SETUP.md: Installation and usage guide
- EXECUTABLE_WHATS_NEW.md: Summary of changes
- install.sh: Automated installation script
- test_executable.sh: Test suite

Features:
- Lexer tokenizes Ark syntax with () for block scoping
- Simple interpreter executes print statements, variables, functions
- Interactive shell with exit() command
- File execution: ark script.ark
- String concatenation with +
- Comment support (// and #)

Ready for Batch 2: AST Node Definitions"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✨ Done! Your changes have been committed and pushed."
