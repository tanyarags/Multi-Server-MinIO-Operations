# MinIO Demo Environment with Docker

This project provides a containerized MinIO demo environment that demonstrates a Python wrapper for MinIO operations. The Docker environment includes everything needed to run the demo.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. Clone this repository or download all files
2. Place your Python scripts in the same directory
3. Run the container using Docker Compose:

```bash
docker-compose up
```

This will build the Docker image and start the container with all necessary environment variables configured.

### Option 2: Using Docker directly

1. Build the Docker image:

```bash
docker build -t minio-demo .
```

2. Run the container:

```bash
docker run -it \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -v $(pwd)/minio_data:/app/minio_data \
  -v $(pwd)/demo_files:/app/demo_files \
  minio-demo
```

## Environment Variables

You can customize the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MINIO_ROOT_USER` | MinIO admin username | minioadmin |
| `MINIO_ROOT_PASSWORD` | MinIO admin password | minioadmin |
| `MINIO_PORT` | MinIO API port | 9000 |
| `MINIO_CONSOLE_PORT` | MinIO Console web UI port | 9001 |

To change these values, edit the `docker-compose.yml` file or provide them on the docker run command.

## Accessing the Demo

The container starts with three tmux sessions:

1. **MinIO Server**: Runs the MinIO server
2. **Demo Script**: Runs the Python demo script
3. **File Explorer**: Terminal for exploring MinIO data directory

### Connecting to tmux sessions

Once the container is running, you can attach to any session:

```bash
# First, get the container ID
docker ps

# Connect to the container
docker exec -it <container_id> bash

# Then attach to any tmux session
tmux attach -t minio-server
tmux attach -t minio-demo
tmux attach -t minio-files
```

To detach from a tmux session, press `Ctrl+B` followed by `D`.

### Accessing MinIO Web Console

You can access the MinIO web console at:
- URL: http://localhost:9001
- Username: minioadmin (or your custom MINIO_ROOT_USER)
- Password: minioadmin (or your custom MINIO_ROOT_PASSWORD)

### Accessing MinIO API

Your applications can access the MinIO API at:
- Endpoint: http://localhost:9000

## File Structure

- `Dockerfile`: Container definition
- `docker-compose.yml`: Docker Compose configuration
- `entrypoint.sh`: Container startup script
- `requirements.txt`: Python dependencies
- `minio_wrapper.py`: Python wrapper for MinIO operations
- `minio_demo.py`: Demo script
- `minio_config.ini`: MinIO connection configuration

## Data Persistence

The container mounts two volumes:

1. `./minio_data:/app/minio_data`: Stores all objects uploaded to MinIO
2. `./demo_files:/app/demo_files`: Shared directory for demo files

These directories will be created on your host system if they don't exist, allowing data to persist between container restarts.

## Customization

### Adding Custom Environment Variables

To add more environment variables, edit the `docker-compose.yml` file:

```yaml
environment:
  - MINIO_ROOT_USER=minioadmin
  - MINIO_ROOT_PASSWORD=minioadmin
  - MINIO_PORT=9000
  - MINIO_CONSOLE_PORT=9001
  - YOUR_CUSTOM_VAR=value
```

Or pass them when running Docker directly:

```bash
docker run -e YOUR_CUSTOM_VAR=value ... minio-demo
```

### Modifying the Python Scripts

If you modify the Python scripts on your host, the changes will be available in the container immediately if you're using the volume mounts specified in docker-compose.yml.

## Troubleshooting

### Container fails to start

Check the Docker logs:

```bash
docker logs minio-demo
```

### Cannot connect to MinIO

Ensure ports 9000 and 9001 are not being used by other applications on your host system.
