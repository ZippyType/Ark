#!/bin/bash
# Batch 21: Binary Builder for Ark

echo "Building Ark executable..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if PyInstaller is available
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
    echo "Run this script again after restarting your computer"
    sudo shutdown -r now
    exit 0
fi

# Try to build
echo "Creating standalone executable..."
pyinstaller --onefile --name ark --console "$SCRIPT_DIR/bin/ark" 2>&1

# Check if it worked
if [ -f "$SCRIPT_DIR/dist/ark" ]; then
    echo "Done! Executable in dist/ark"
    chmod +x "$SCRIPT_DIR/dist/ark"
else
    echo ""
    echo "Build failed (Python shared library issue)"
    echo ""
    echo "Alternative: Use python directly:"
    echo "  python3 bin/ark file.ark"
    echo ""
    echo "Or create a launcher script:"
    echo '#!/bin/bash'
    echo 'exec python3 /path/to/ark/bin/ark "$@"'
fi