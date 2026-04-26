#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BIN_DIR="$SCRIPT_DIR/bin"
ARK_BIN="$BIN_DIR/ark"
EXT_DIR="$SCRIPT_DIR/extensions/ark-lang"

if [ ! -f "$ARK_BIN" ]; then
    echo "Error: ark binary not found at $ARK_BIN"
    exit 1
fi

if [ ! -d "$EXT_DIR" ]; then
    echo "Error: ark-lang extension not found at $EXT_DIR"
    exit 1
fi

chmod +x "$ARK_BIN"

# Setup PATH in shell config files
PROFILE_FILE="$HOME/.profile"
BASHRC_FILE="$HOME/.bashrc"
ZSHRC_FILE="$HOME/.zshrc"
FISH_CONFIG="$HOME/.config/fish/config.fish"

add_path_to_file() {
    local file="$1"
    local path_line='export PATH="'"$BIN_DIR"':$PATH"'
    if [ -f "$file" ]; then
        if ! grep -q "ark-lang" "$file" 2>/dev/null; then
            echo "$path_line" >> "$file"
        fi
    else
        echo "$path_line" >> "$file"
    fi
}

add_path_to_file "$PROFILE_FILE"
add_path_to_file "$BASHRC_FILE"
add_path_to_file "$ZSHRC_FILE"

# Try to add to fish config
if [ -d "$HOME/.config/fish" ]; then
    if [ ! -f "$FISH_CONFIG" ]; then
        mkdir -p "$HOME/.config/fish"
        touch "$FISH_CONFIG"
    fi
    if ! grep -q "ark-lang" "$FISH_CONFIG" 2>/dev/null; then
        echo 'set -gx PATH $PATH '"$BIN_DIR" >> "$FISH_CONFIG"
    fi
fi

# Try to link to /usr/local/bin (requires root)
if [ -L "/usr/local/bin/ark" ] 2>/dev/null || [ -f "/usr/local/bin/ark" ] 2>/dev/null; then
    echo "Warning: /usr/local/bin/ark already exists"
else
    if ln -sf "$ARK_BIN" "/usr/local/bin/ark" 2>/dev/null; then
        echo "Installed ark to /usr/local/bin/ark"
    else
        echo "Added $BIN_DIR to PATH in shell config files"
    fi
fi

# Install VS Code extension
VSCODE_EXT_DIR="$HOME/.vscode/extensions"
mkdir -p "$VSCODE_EXT_DIR"
EXT_TARGET="$VSCODE_EXT_DIR/ark-lang"

if [ -d "$EXT_TARGET" ]; then
    echo "VS Code extension already installed at $EXT_TARGET"
else
    cp -r "$EXT_DIR" "$VSCODE_EXT_DIR"
    echo "VS Code extension installed to $EXT_TARGET"
fi

# Refresh bashrc
source ~/.bashrc

echo ""
echo "============================================"
echo "     === Installation Complete ==="
echo "============================================"
echo ""
echo "Installed:"
echo "  ✓ ark command"
echo "  ✓ VS Code extension (ark-lang)"
echo ""
echo "Use:"
echo "  ark file.ark          - Run an Ark file"
echo "  ark -c 'code'     - Run code from command line"
echo "  ark               - Interactive shell"
echo ""
echo "Restart VS Code or run 'Extensions: Reload Window'"
echo "to activate the Ark language extension."
echo ""
echo "Enjoy Ark! 🦕"