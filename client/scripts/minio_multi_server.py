#!/usr/bin/env python3
import os
import sys
import configparser
import argparse
from minio_wrapper import MinioWrapper

def load_config(config_file):
    """
    Load MinIO server configurations from config file.
    
    Args:
        config_file (str): Path to the configuration file
        
    Returns:
        dict: Dictionary with server configurations
    """
    if not os.path.exists(config_file):
        print(f"Error: Config file {config_file} not found")
        sys.exit(1)
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    servers = {}
    for section in config.sections():
        servers[section] = {
            'endpoint': config[section]['endpoint'],
            'access_key': config[section]['access_key'],
            'secret_key': config[section]['secret_key'],
            'secure': config[section].getboolean('secure', fallback=False),
            'bucket_name': config[section]['bucket_name']
        }
    
    return servers

def initialize_clients(server_configs):
    """
    Initialize MinIO clients for all servers in the configuration.
    
    Args:
        server_configs (dict): Dictionary with server configurations
        
    Returns:
        dict: Dictionary with MinioWrapper instances for each server
    """
    clients = {}
    for server_name, config in server_configs.items():
        try:
            clients[server_name] = MinioWrapper(
                config['endpoint'],
                config['access_key'],
                config['secret_key'],
                config['secure'],
                config['bucket_name']
            )
            print(f"Connected to {server_name} at {config['endpoint']}")
        except Exception as e:
            print(f"Error connecting to {server_name}: {e}")
    
    return clients

def upload_to_all_servers(clients, file_path, object_name=None):
    """
    Upload a file to all MinIO servers.
    
    Args:
        clients (dict): Dictionary with MinioWrapper instances
        file_path (str): Path to the local file
        object_name (str, optional): Name of the object in MinIO
        
    Returns:
        dict: Dictionary with upload results for each server
    """
    results = {}
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return {server: False for server in clients}
    
    # Use filename as object_name if not specified
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    print(f"\n--- Uploading {file_path} as {object_name} to all servers ---")
    
    for server_name, client in clients.items():
        print(f"\nUploading to {server_name}...")
        success = client.upload_file(file_path, object_name)
        results[server_name] = success
    
    # Summary
    print("\n--- Upload Summary ---")
    success_count = sum(1 for success in results.values() if success)
    print(f"Uploaded to {success_count} out of {len(results)} servers.")
    
    for server, success in results.items():
        status = "Success" if success else "Failed"
        print(f"  {server}: {status}")
    
    return results

def download_from_all_servers(clients, object_name, output_dir=None):
    """
    Download a file from all MinIO servers.
    
    Args:
        clients (dict): Dictionary with MinioWrapper instances
        object_name (str): Name of the object in MinIO
        output_dir (str, optional): Directory to save the downloaded files
        
    Returns:
        dict: Dictionary with download results for each server
    """
    results = {}
    
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n--- Downloading {object_name} from all servers ---")
    
    for server_name, client in clients.items():
        print(f"\nDownloading from {server_name}...")
        
        # Create server-specific filename to avoid overwriting
        if output_dir:
            file_path = os.path.join(output_dir, f"{server_name}_{object_name}")
        else:
            file_path = f"{server_name}_{object_name}"
        
        success = client.download_file(object_name, file_path)
        results[server_name] = success
    
    # Summary
    print("\n--- Download Summary ---")
    success_count = sum(1 for success in results.values() if success)
    print(f"Downloaded from {success_count} out of {len(results)} servers.")
    
    for server, success in results.items():
        status = "Success" if success else "Failed"
        print(f"  {server}: {status}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Multi-server MinIO operations')
    parser.add_argument('--config', '-c', required=True, help='Path to the config file')
    parser.add_argument('--action', '-a', required=True, choices=['upload', 'download', 'both'], 
                       help='Action to perform: upload, download, or both')
    parser.add_argument('--file', '-f', help='File to upload (required for upload)')
    parser.add_argument('--object', '-o', help='Object name in MinIO (uses filename if not specified)')
    parser.add_argument('--output-dir', '-d', help='Directory to save downloaded files')
    
    args = parser.parse_args()
    
    # Load server configurations
    server_configs = load_config(args.config)
    
    # Initialize clients for all servers
    clients = initialize_clients(server_configs)
    
    if not clients:
        print("Error: No MinIO clients could be initialized. Exiting.")
        sys.exit(1)
    
    # Determine object name
    object_name = args.object
    if args.action in ['upload', 'both'] and args.file:
        if not object_name:
            object_name = os.path.basename(args.file)
    
    # Perform requested actions
    if args.action in ['upload', 'both']:
        if not args.file:
            print("Error: File path is required for upload operation")
            sys.exit(1)
        upload_to_all_servers(clients, args.file, object_name)
    
    if args.action in ['download', 'both']:
        if not object_name:
            print("Error: Object name is required for download operation")
            sys.exit(1)
        download_from_all_servers(clients, object_name, args.output_dir)

if __name__ == "__main__":
    main()
