# Multi-Server MinIO Operations

A system for managing file operations across multiple MinIO object storage servers. This project provides a Docker-based environment with multiple MinIO servers and a client application that can upload and download files across all servers.

## Overview

This project sets up:
- Three MinIO object storage servers (named NG, TZ, and ZM)
- A Python client with a wrapper library for simplified MinIO operations
- Scripts for batch operations across all servers

## Features

- Concurrent file uploads to multiple MinIO servers
- Concurrent file downloads from multiple MinIO servers
- Consistent bucket management across servers
- Detailed operation logging and summaries
- Configurable server endpoints, credentials, and settings

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git (for cloning the repository)

### Installation

1. Clone the repository:
   ```bash
   https://github.com/tanyarags/Multi-Server-MinIO-Operations.git
   cd Multi-Server-MinIO-Operations
   ```

2. Create the directory structure:
   ```bash
   mkdir -p client/scripts client/config client/demo_files
   mkdir -p server-ng/data server-ng/config
   mkdir -p server-tz/data server-tz/config
   mkdir -p server-zm/data server-zm/config
   ```

3. Deploy the files from this repository to their respective locations.

4. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

### Configuration

Edit `client/config/minio_config_multi.ini` to configure your MinIO servers:

```ini
[NG]
endpoint = minio-server-ng:9000
access_key = minioadmin
secret_key = minioadmin
secure = False
bucket_name = demo-bucket

[TZ]
endpoint = minio-server-tz:9000
access_key = minioadmin
secret_key = minioadmin
secure = False
bucket_name = demo-bucket

[ZM]
endpoint = minio-server-zm:9000
access_key = minioadmin
secret_key = minioadmin
secure = False
bucket_name = demo-bucket
```

## Usage

### Uploading Files

To upload a file to all configured MinIO servers:

```bash
docker exec -it minio-client /app/scripts/minio-script-multi3.sh upload /app/demo_files/example.txt my-object-name.txt
```

### Downloading Files

To download a file from all configured MinIO servers:

```bash
docker exec -it minio-client /app/scripts/minio-script-multi3.sh download my-object-name.txt /app/downloads
```

### Upload and Download in One Operation

To both upload and download in a single operation:

```bash
docker exec -it minio-client /app/scripts/minio-script-multi3.sh both /app/demo_files/example.txt my-object-name.txt /app/downloads
```

## Project Structure

```
├── client/
│   ├── scripts/
│   │   ├── minio_wrapper.py        # MinIO client wrapper class
│   │   ├── minio_multi_server.py   # Multi-server operations
│   │   └── minio-script-multi3.sh  # Command-line script
│   ├── config/
│   │   └── minio_config_multi.ini  # Server configurations
│   ├── demo_files/                 # Sample files for testing
│   └── Dockerfile                  # Client container definition
├── server-ng/                      # Data and config for NG server
├── server-tz/                      # Data and config for TZ server
├── server-zm/                      # Data and config for ZM server
└── docker-compose.yml              # Container orchestration
```

## Architecture

### Containers

- **minio-server-ng**: MinIO server for the NG region
  - Web UI: http://localhost:9001
  - API: http://localhost:9000

- **minio-server-tz**: MinIO server for the TZ region
  - Web UI: http://localhost:9011
  - API: http://localhost:9010

- **minio-server-zm**: MinIO server for the ZM region
  - Web UI: http://localhost:9021
  - API: http://localhost:9020

- **minio-client**: Python container for running operations
  - Contains the scripts and configurations for interacting with the servers

### Components

- **MinioWrapper**: A Python class that wraps the MinIO SDK
  - Simplifies common operations
  - Handles error conditions gracefully

- **Multi-Server Operations**: Python script that manages concurrent operations
  - Uploads to all servers in parallel
  - Downloads from all servers with server-specific naming
  - Provides operation summaries

## Technical Details

### MinioWrapper Class

This class provides a simplified interface to the MinIO SDK:

```python
# Initialize a client
client = MinioWrapper(
    endpoint="minio-server:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
    bucket_name="demo-bucket"
)

# Upload a file
client.upload_file("/path/to/local/file.txt", "remote-name.txt")

# Download a file
client.download_file("remote-name.txt", "/path/to/save/file.txt")
```

### Multi-Server Operations

The multi-server script handles operations across all configured servers:

```python
# Load configurations
configs = load_config("config.ini")

# Initialize clients
clients = initialize_clients(configs)

# Upload to all servers
results = upload_to_all_servers(clients, "/path/to/file.txt", "object-name.txt")

# Download from all servers
results = download_from_all_servers(clients, "object-name.txt", "/output/dir")
```

