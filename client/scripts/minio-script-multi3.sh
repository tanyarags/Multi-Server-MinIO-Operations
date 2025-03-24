#!/bin/bash

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <action> [file_path] [object_name] [output_dir]"
    echo ""
    echo "Actions:"
    echo "  upload   - Upload a file to all MinIO servers"
    echo "  download - Download a file from all MinIO servers"
    echo "  both     - Upload and then download a file"
    echo ""
    echo "Examples:"
    echo "  $0 upload /app/demo_files/example.txt custom-name.txt"
    echo "  $0 download custom-name.txt /app/downloads"
    echo "  $0 both /app/demo_files/example.txt custom-name.txt /app/downloads"
    exit 1
fi

ACTION=$1
FILE_PATH=${2:-""}
OBJECT_NAME=${3:-""}
OUTPUT_DIR=${4:-""}

# Config file path
CONFIG_FILE="/app/config/minio_config_multi.ini"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

# Execute the Python script with appropriate arguments
if [ "$ACTION" == "upload" ]; then
    if [ -z "$FILE_PATH" ]; then
        echo "Error: File path is required for upload operation"
        exit 1
    fi
    
    # Run upload operation
    python3 /app/scripts/minio_multi_server.py \
        --config "$CONFIG_FILE" \
        --action upload \
        --file "$FILE_PATH" \
        ${OBJECT_NAME:+--object "$OBJECT_NAME"}

elif [ "$ACTION" == "download" ]; then
    if [ -z "$OBJECT_NAME" ]; then
        echo "Error: Object name is required for download operation"
        exit 1
    fi
    
    # Run download operation
    python3 /app/scripts/minio_multi_server.py \
        --config "$CONFIG_FILE" \
        --action download \
        --object "$OBJECT_NAME" \
        ${OUTPUT_DIR:+--output-dir "$OUTPUT_DIR"}

elif [ "$ACTION" == "both" ]; then
    if [ -z "$FILE_PATH" ]; then
        echo "Error: File path is required for upload operation"
        exit 1
    fi
    
    # If object name is not provided, use filename
    if [ -z "$OBJECT_NAME" ]; then
        OBJECT_NAME=$(basename "$FILE_PATH")
    fi
    
    # Run both operations
    python3 /app/scripts/minio_multi_server.py \
        --config "$CONFIG_FILE" \
        --action both \
        --file "$FILE_PATH" \
        --object "$OBJECT_NAME" \
        ${OUTPUT_DIR:+--output-dir "$OUTPUT_DIR"}
else
    echo "Error: Invalid action '$ACTION'. Use 'upload', 'download', or 'both'."
    exit 1
fi

# Exit with the same status as the Python script
exit $?
