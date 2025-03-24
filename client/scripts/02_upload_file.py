#!/usr/bin/env python3
"""
Script 2: Upload a file to MinIO

This script demonstrates how to:
1. Create a sample file
2. Upload it to MinIO
3. Confirm upload was successful
"""

import os
import sys
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

def create_sample_file():
    """Create a sample text file for upload"""
    # Create demo_files directory if it doesn't exist
    os.makedirs("../demo_files", exist_ok=True)
    
    # Create a sample file
    filename = "../demo_files/sample_text.txt"
    with open(filename, "w") as f:
        f.write("This is a sample file created for the MinIO demo.\n")
        f.write("It contains some text that will be uploaded to MinIO.\n")
        f.write(f"Created at: {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n")
        f.write("This file demonstrates a simple upload operation.")
    
    logger.info(f"Created sample file: {filename}")
    return filename

def upload_file():
    """Upload a file to MinIO"""
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
        file_path = create_sample_file()
        
        # Get the file name without the path
        file_name = os.path.basename(file_path)
        
        # Upload the file
        logger.info(f"Uploading file {file_path} to bucket {bucket_name} as {file_name}")
        client.fput_object(bucket_name, file_name, file_path)
        logger.info(f"Upload successful: {file_name}")
        
        # Check if the file exists in the bucket
        try:
            # Get stats for the object
            stat = client.stat_object(bucket_name, file_name)
            logger.info(f"File found in bucket: {file_name}")
            logger.info(f"Size: {stat.size} bytes")
            logger.info(f"Last modified: {stat.last_modified}")
            logger.info(f"ETag: {stat.etag}")
            return True
        except Exception as e:
            logger.error(f"Could not verify file: {e}")
            return False
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Uploading a File ===")
    success = upload_file()
    print("=" * 40)
    if success:
        print("✅ File upload completed successfully")
    else:
        print("❌ File upload failed")
