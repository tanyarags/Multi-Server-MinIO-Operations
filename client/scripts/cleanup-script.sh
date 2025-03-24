#!/bin/bash
# Cleanup script for MinIO demo

echo "=== MinIO Demo: Cleanup ==="
echo "This script will clean up the local files and directories created during the demo."
echo "Note: This will NOT delete objects from the MinIO server."

# Function to confirm before proceeding
confirm() {
    read -p "Are you sure you want to continue? [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Check for confirmation
if ! confirm; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Cleaning up demo files..."

# Clean up the demo_files directory
if [ -d "../demo_files" ]; then
    echo "- Removing demo_files directory"
    rm -rf "../demo_files"
fi

echo "Cleanup completed."
echo "Note: Objects in MinIO server still exist. Use the MinIO Console or"
echo "script 09_delete_object.py to remove specific objects if needed."
