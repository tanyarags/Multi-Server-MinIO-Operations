#!/usr/bin/env python3
"""
Script 8: Working with object metadata in MinIO

This script demonstrates how to:
1. Upload a file with custom metadata
2. Retrieve and display object metadata
3. Update metadata (by re-uploading an object)
"""

import os
import sys
import json
import logging
from datetime import datetime
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

def create_metadata_file():
    """Create a sample file with metadata"""
    # Create demo_files directory if it doesn't exist
    os.makedirs("../demo_files", exist_ok=True)
    
    # Create a sample file
    filename = "../demo_files/metadata_sample.txt"
    with open(filename, "w") as f:
        f.write("This is a sample file to demonstrate metadata handling in MinIO.\n")
        f.write(f"Created at: {datetime.now().isoformat()}\n")
        f.write("This file will have custom metadata attached to it in MinIO.\n")
    
    logger.info(f"Created sample file: {filename}")
    return filename

def work_with_metadata():
    """Upload and work with object metadata in MinIO"""
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
        
        # Ensure bucket exists
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created")
        
        # Create a sample file
        file_path = create_metadata_file()
        object_name = "metadata_demo.txt"
        
        # Define custom metadata - Note: MinIO requires 'x-amz-meta-' prefix
        # When using put_object, we include this prefix
        metadata = {
            "x-amz-meta-author": "MinIO Demo",
            "x-amz-meta-created-by": "metadata_demo.py",
            "x-amz-meta-purpose": "demonstrate metadata handling",
            "x-amz-meta-version": "1.0",
            "Content-Type": "text/plain"
        }
        
        # Upload the file with metadata
        logger.info(f"Uploading file {file_path} to {object_name} with metadata")
        with open(file_path, 'rb') as file_data:
            file_stat = os.stat(file_path)
            client.put_object(
                bucket_name, 
                object_name,
                file_data, 
                file_stat.st_size,
                metadata=metadata
            )
        logger.info(f"Upload successful with metadata")
        
        # Retrieve and display the object's metadata
        logger.info(f"Retrieving metadata for {object_name}")
        stat = client.stat_object(bucket_name, object_name)
        
        print("\nObject metadata:")
        print(f"Object: {object_name}")
        print(f"Size: {stat.size} bytes")
        print(f"Last modified: {stat.last_modified}")
        print(f"ETag: {stat.etag}")
        print("\nCustom metadata:")
        
        # Display all metadata
        for key, value in stat.metadata.items():
            # When retrieving metadata, MinIO normalizes the keys to lowercase
            # and removes the 'x-amz-meta-' prefix
            print(f"- {key}: {value}")
        
        # Update metadata by re-uploading the object
        updated_metadata = {
            "x-amz-meta-author": "MinIO Demo",
            "x-amz-meta-created-by": "metadata_demo.py",
            "x-amz-meta-purpose": "demonstrate metadata handling",
            "x-amz-meta-version": "2.0",  # Updated version
            "x-amz-meta-updated-at": datetime.now().isoformat(),  # New field
            "Content-Type": "text/plain"
        }
        
        logger.info(f"Updating metadata for {object_name}")
        with open(file_path, 'rb') as file_data:
            file_stat = os.stat(file_path)
            client.put_object(
                bucket_name, 
                object_name,
                file_data, 
                file_stat.st_size,
                metadata=updated_metadata
            )
        logger.info(f"Metadata update successful")
        
        # Retrieve and display the updated metadata
        updated_stat = client.stat_object(bucket_name, object_name)
        
        print("\nUpdated object metadata:")
        print(f"Object: {object_name}")
        print(f"Size: {updated_stat.size} bytes")
        print(f"Last modified: {updated_stat.last_modified}")
        print(f"ETag: {updated_stat.etag}")
        print("\nUpdated custom metadata:")
        
        # Display all updated metadata
        for key, value in updated_stat.metadata.items():
            print(f"- {key}: {value}")
        
        # Download the metadata file to verify
        download_dir = "../demo_files/metadata"
        os.makedirs(download_dir, exist_ok=True)
        download_path = os.path.join(download_dir, object_name)
        
        logger.info(f"Downloading object to {download_path}")
        client.fget_object(bucket_name, object_name, download_path)
        
        if os.path.exists(download_path):
            logger.info(f"Download successful: {download_path}")
            
            # Display file contents
            print("\nFile contents:")
            print("-" * 40)
            with open(download_path, 'r') as f:
                print(f.read())
            print("-" * 40)
        
        return True
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Working with Object Metadata ===")
    success = work_with_metadata()
    print("=" * 50)
    if success:
        print("✅ Metadata operations completed successfully")
    else:
        print("❌ Metadata operations failed")
