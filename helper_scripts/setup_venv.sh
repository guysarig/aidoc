#!/bin/bash
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

echo "Current directory: $(pwd) 's contents:"
ls -l */ -d
