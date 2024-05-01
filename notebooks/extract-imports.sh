#!/bin/bash

# Check if a file path is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_python_file>"
    exit 1
fi

# File path
FILE=$1

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File does not exist."
    exit 1
fi

# Extract lines that start with 'import' or 'from'
grep -E "^import |^from " "$FILE"
