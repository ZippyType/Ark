#!/bin/bash

# Ark Programming Language - Installation Script for Ubuntu/Linux
# This script sets up the Ark executable in your system PATH

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Ark Language Installation ===${NC}"

# Detect the repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARK_ROOT="$SCRIPT_DIR"

echo "Ark directory: $ARK_ROOT"

# Make the ark executable
chmod +x "$ARK_ROOT/ark"
echo -e "${GREEN}✓ Made ark executable${NC}"

# Option 1: Create symlink in /usr/local/bin (requires sudo)
if [ -w /usr/local/bin ]; then
    sudo ln -sf "$ARK_ROOT/ark" /usr/local/bin/ark
    echo -e "${GREEN}✓ Installed to /usr/local/bin/ark (system-wide)${NC}"
else
    # Option 2: Add to user's local bin
    mkdir -p "$HOME/.local/bin"
    ln -sf "$ARK_ROOT/ark" "$HOME/.local/bin/ark"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        echo -e "${GREEN}✓ Installed to ~/.local/bin/ark${NC}"
    else
        echo -e "${BLUE}Adding ~/.local/bin to PATH...${NC}"
        
        # Add to bashrc
        if ! grep -q '~/.local/bin' ~/.bashrc; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        fi
        
        # Add to zshrc if it exists
        if [ -f ~/.zshrc ]; then
            if ! grep -q '~/.local/bin' ~/.zshrc; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
            fi
        fi
        
        echo -e "${GREEN}✓ Installed to ~/.local/bin/ark${NC}"
        echo -e "${BLUE}⚠ Run: source ~/.bashrc (or source ~/.zshrc)${NC}"
    fi
fi

# Verify installation
echo ""
echo -e "${BLUE}Verifying installation...${NC}"
if command -v ark &> /dev/null; then
    echo -e "${GREEN}✓ ark is available in PATH${NC}"
    ark --version 2>/dev/null || echo "  (Ready to use)"
else
    echo -e "${BLUE}⚠ ark not yet in PATH. Reload your shell:${NC}"
    echo "    source ~/.bashrc"
fi

echo ""
echo -e "${GREEN}=== Installation Complete ===${NC}"
echo ""
echo -e "Usage:"
echo -e "  ${GREEN}ark${NC}                    # Start interactive shell"
echo -e "  ${GREEN}ark script.ark${NC}         # Run a script"
echo -e ""
echo -e "Try: ${GREEN}ark examples/hello.ark${NC}"
