#!/bin/bash
# Client container entrypoint script with tmux support

# Display welcome message
echo "========================================"
echo "MinIO Client - Docker Environment"
echo "========================================"
echo "Using configuration from minio_config.ini"
echo "========================================"

# Check if config file exists
if [ ! -f "minio_config.ini" ]; then
    echo "ERROR: minio_config.ini not found!"
    echo "Please make sure the config file is mounted to the container."
    exit 1
fi

# Install tmux if not already installed
if ! command -v tmux &> /dev/null; then
    echo "Installing tmux..."
    apt-get update && apt-get install -y tmux
fi

# Read values from config file to display
if command -v python &> /dev/null; then
    echo "Configuration summary:"
    python -c "
import configparser
config = configparser.ConfigParser()
config.read('minio_config.ini')
print(f\"- Server: {config['minio']['endpoint']}\")
print(f\"- Bucket: {config['minio']['bucket_name']}\")
print(f\"- Secure: {config['minio']['secure']}\")
"
fi

# Function to check if MinIO server is ready
wait_for_minio() {
    # Parse the endpoint from config file
    SERVER_ENDPOINT=$(grep -A3 '^\[minio\]' minio_config.ini | grep 'endpoint' | cut -d '=' -f2 | tr -d ' ')
    echo "Waiting for MinIO server at $SERVER_ENDPOINT to be ready..."
    
    # Extract hostname and port from endpoint
    MINIO_HOST=$(echo $SERVER_ENDPOINT | cut -d':' -f1)
    MINIO_PORT=$(echo $SERVER_ENDPOINT | cut -d':' -f2)
    
    until curl -s "http://$MINIO_HOST:$MINIO_PORT/minio/health/live" > /dev/null; do
        echo "MinIO server is not ready yet... waiting 3 seconds"
        sleep 3
    done
    echo "MinIO server is ready!"
}

# Wait for MinIO server to be ready
wait_for_minio

# Check if scripts directory exists
if [ ! -d "/app/scripts" ]; then
    echo "Creating scripts directory..."
    mkdir -p /app/scripts
fi

# Handle demo mode detection and execution
if [ "$1" = "demo" ] || [ "$MINIO_DEMO_MODE" = "true" ]; then
    echo "Starting MinIO demo in tmux session..."
    
    # Check if the tmux demo script exists
    if [ -f "/app/run_demo_tmux.sh" ]; then
        # Make it executable
        chmod +x /app/run_demo_tmux.sh
        
        # Run the tmux demo script
        /app/run_demo_tmux.sh
    elif [ -f "/app/scripts/run_demo_tmux.sh" ]; then
        # Make it executable
        chmod +x /app/scripts/run_demo_tmux.sh
        
        # Run the tmux demo script from scripts directory
        /app/scripts/run_demo_tmux.sh
    else
        echo "tmux demo script not found, running standard demo script..."
        
        # Check if the standard demo script exists
        if [ -f "/app/scripts/run_demo.sh" ]; then
            chmod +x /app/scripts/run_demo.sh
            cd /app/scripts && ./run_demo.sh
        else
            echo "Demo script not found! Please check your configuration."
            echo "Starting bash shell instead..."
            exec bash
        fi
    fi
else
    echo ""
    echo "MinIO client container is ready."
    echo "To run the demo script manually: python scripts/run_demo.py"
    echo "To run the tmux demo: bash run_demo_tmux.sh"
    echo "To run custom scripts: python scripts/your_script.py"
    echo ""
    echo "Available demo modes:"
    echo "1. Standard script mode: bash scripts/run_demo.sh"
    echo "2. tmux session mode: bash run_demo_tmux.sh"
    echo ""
    exec bash
fi
