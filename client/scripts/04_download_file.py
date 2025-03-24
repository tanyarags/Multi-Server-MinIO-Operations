#!/usr/bin/env python3
"""
Script 4: Download a file from MinIO

This script demonstrates how to:
1. Connect to a MinIO server
2. Download a file from a bucket
3. Verify the download
4. Display the file contents
"""

import os
import sys
import logging
from minio import Minio
from minio.error import S3Error

# Add parent directory to path to import the wrapper
sys.path.append('..')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_file():
    """Download a file from MinIO"""
    try:
        # Read config from the config file
        import configparser
        config = configparser.ConfigParser()
        config.read('../minio_config.ini')
        
        # Extract connection parameters
        endpoint = config['minio']['endpoint']
        access_key = config['minio']['access_key']
        secret_key = config['minio']['secret_key']
        secure = config['minio'].getboolean('secure')
        bucket_name = config['minio']['bucket_name']
        
        # Initialize MinIO client
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        # Check if bucket exists
        if not client.bucket_exists(bucket_name):
            logger.error(f"Bucket '{bucket_name}' does not exist")
            return False
        
        # List all objects to let user choose which to download
        objects = list(client.list_objects(bucket_name, recursive=True))
        
        if not objects:
            logger.error(f"Bucket '{bucket_name}' is empty")
            print(f"\nBucket '{bucket_name}' is empty. Please upload some files first.")
            return False
        
        # For simplicity, just download the first object
        # In a real application, you might want to let the user choose
        object_name = objects[0].object_name
        
        # Create downloads directory if it doesn't exist
        download_dir = "../demo_files/downloads"
        os.makedirs(download_dir, exist_ok=True)
        
        # Set local file path
        download_path = os.path.join(download_dir, object_name)
        
        # Ensure directory exists for the download
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        
        # Download the file
        logger.info(f"Downloading '{object_name}' to '{download_path}'")
        client.fget_object(bucket_name, object_name, download_path)
        logger.info(f"Download successful")
        
        # Verify file exists
        if os.path.exists(download_path):
            logger.info(f"File successfully downloaded to {download_path}")
            
            # Get file stats
            size = os.path.getsize(download_path)
            
            # Print file info
            print(f"\nFile downloaded: {object_name}")
            print(f"Saved to: {download_path}")
            print(f"Size: {size} bytes")
            
            # Display file contents if it's a text file
            if object_name.endswith('.txt'):
                print("\nFile contents:")
                print("-" * 40)
                with open(download_path, 'r') as f:
                    print(f.read())
                print("-" * 40)
            
            return True
        else:
            logger.error(f"Download verification failed: file not found at {download_path}")
            return False
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Downloading a File ===")
    success = download_file()
    print("=" * 40)
    if success:
        print("✅ File download completed successfully")
    else:
        print("❌ File download failed")
