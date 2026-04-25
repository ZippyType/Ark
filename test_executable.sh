#!/bin/bash

# Ark Executable - Test Suite
# This script tests the Ark executable and shell to make sure everything works

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           ARK EXECUTABLE - TEST SUITE                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARK_CMD="python3 $SCRIPT_DIR/ark"

echo "Testing with: $ARK_CMD"
echo ""

# Test 1: Version check
echo "TEST 1: Version Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$ARK_CMD --version
echo "✓ Version check works"
echo ""

# Test 2: Help check
echo "TEST 2: Help Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$ARK_CMD --help | head -5
echo "✓ Help display works"
echo ""

# Test 3: Execute hello.ark
echo "TEST 3: Execute examples/hello.ark"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$ARK_CMD examples/hello.ark
echo "✓ File execution works"
echo ""

# Test 4: Execute variables.ark
echo "TEST 4: Execute examples/variables.ark"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$ARK_CMD examples/variables.ark | head -10
echo "✓ Multiple expressions work"
echo ""

# Test 5: Execute functions.ark
echo "TEST 5: Execute examples/functions.ark"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$ARK_CMD examples/functions.ark | head -10
echo "✓ Function definitions work"
echo ""

# Test 6: Test with single line input (simulated)
echo "TEST 6: Single Line Execution"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo 'let test = 42' > /tmp/test_single.ark
$ARK_CMD /tmp/test_single.ark
echo "✓ Single line code works"
echo ""

# Test 7: Check if lexer module is available
echo "TEST 7: Module Import Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); from lexer import lex; print('✓ Lexer module found')"
echo ""

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ALL TESTS PASSED! ✓                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "You can now use the Ark executable:"
echo "  $ARK_CMD                    # Start interactive shell"
echo "  $ARK_CMD examples/hello.ark  # Run a script"
echo ""
echo "Or install it globally:"
echo "  bash install.sh"
echo ""
