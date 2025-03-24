#!/usr/bin/env python3
"""
Script 7: Recover a deleted local file from MinIO

This script demonstrates how to:
1. Identify a file that was deleted locally
2. Recover it from MinIO storage
3. Verify the recovery was successful
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

def recover_file():
    """Recover a deleted local file from MinIO"""
    try:
        # Check if we have info about the deleted file
        deleted_file_info = "../demo_files/deleted_file_info.txt"
        if not os.path.exists(deleted_file_info):
            logger.error(f"Deleted file info not found at '{deleted_file_info}'")
            print("\nPlease run script 06_delete_local_file.py first to simulate data loss")
            return False
        
        # Read the deleted file path
        with open(deleted_file_info, "r") as f:
            deleted_file_path = f.read().strip()
        
        if not deleted_file_path:
            logger.error("Deleted file path is empty")
            return False
        
        # Extract the object name from the path
        # The format is typically "../demo_files/downloads/object_name"
        download_dir = "../demo_files/downloads/"
        if download_dir in deleted_file_path:
            object_name = deleted_file_path.replace(download_dir, "")
        else:
            object_name = os.path.basename(deleted_file_path)
        
        logger.info(f"Attempting to recover object: {object_name}")
        
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
        
        # Check if the object exists in MinIO
        try:
            client.stat_object(bucket_name, object_name)
            logger.info(f"Object '{object_name}' found in bucket '{bucket_name}'")
        except:
            logger.error(f"Object '{object_name}' not found in bucket '{bucket_name}'")
            print(f"\nCould not find '{object_name}' in MinIO bucket")
            return False
        
        # Create recovery directory if it doesn't exist
        recovery_dir = "../demo_files/recovery"
        os.makedirs(recovery_dir, exist_ok=True)
        
        # Set recovery file path
        recovery_path = os.path.join(recovery_dir, os.path.basename(object_name))
        
        # Download the file from MinIO
        logger.info(f"Recovering '{object_name}' to '{recovery_path}'")
        client.fget_object(bucket_name, object_name, recovery_path)
        
        # Verify recovery
        if os.path.exists(recovery_path):
            logger.info(f"File successfully recovered to {recovery_path}")
            
            # Get file stats
            size = os.path.getsize(recovery_path)
            
            # Print recovery info
            print(f"\nFile recovered successfully!")
            print(f"Original file path: {deleted_file_path}")
            print(f"Recovered to: {recovery_path}")
            print(f"Size: {size} bytes")
            
            # Display file contents if it's a text file
            if recovery_path.endswith('.txt'):
                print("\nRecovered file contents:")
                print("-" * 40)
                with open(recovery_path, 'r') as f:
                    print(f.read())
                print("-" * 40)
            
            # Also restore the original file for completeness
            os.makedirs(os.path.dirname(deleted_file_path), exist_ok=True)
            
            logger.info(f"Also restoring to original location: {deleted_file_path}")
            with open(recovery_path, 'rb') as src, open(deleted_file_path, 'wb') as dst:
                dst.write(src.read())
            
            if os.path.exists(deleted_file_path):
                logger.info(f"Original file restored at {deleted_file_path}")
                print(f"\nAlso restored to original location: {deleted_file_path}")
            
            return True
        else:
            logger.error(f"Recovery verification failed: file not found at {recovery_path}")
            return False
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Recovering Deleted File ===")
    success = recover_file()
    print("=" * 40)
    if success:
        print("✅ File recovered successfully from MinIO")
        print("\nThis demonstrates how MinIO can be used to recover lost data")
    else:
        print("❌ File recovery failed")
