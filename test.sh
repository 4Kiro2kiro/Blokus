#!/bin/sh

# Set error handling
set -e

# Print header
printf "=== Running Blokus Game Tests ===\n\n"

# Add the src directory to PYTHONPATH so tests can import the game package
PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export PYTHONPATH

# Run the tests with Python's unittest
python3 -m unittest test/test_game.py -v

# Check the exit status
if [ $? -eq 0 ]; then
    printf "\n=== All tests passed successfully! ===\n"
else
    printf "\n=== Some tests failed! ===\n"
    exit 1
fi
