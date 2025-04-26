#!/bin/sh


# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check Python 3 installation
if ! command -v python3 > /dev/null 2>&1; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check rclone installation
if ! command -v rclone > /dev/null 2>&1; then
    echo "Error: rclone is required but not installed."
    exit 1
fi

python3 "$SCRIPT_DIR/src/argus.py" "$@" 