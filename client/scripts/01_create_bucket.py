#!/usr/bin/env python3
"""
Script 1: Create a bucket in MinIO

This script demonstrates how to:
1. Connect to a MinIO server
2. Create a new bucket
3. Verify that the bucket exists
"""

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

def create_bucket():
    """Create a new bucket in MinIO"""
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
        
        logger.info(f"Connecting to MinIO server at {endpoint}")
        logger.info(f"Using bucket name: {bucket_name}")
        
        # Initialize MinIO client
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        # Check if bucket already exists
        if client.bucket_exists(bucket_name):
            logger.info(f"Bucket '{bucket_name}' already exists")
        else:
            # Create the bucket
            client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully")
        
        # List all buckets to verify
        buckets = client.list_buckets()
        logger.info("List of buckets:")
        for bucket in buckets:
            logger.info(f"- {bucket.name} (created: {bucket.creation_date})")
        
        return True
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Creating a Bucket ===")
    success = create_bucket()
    print("=" * 40)
    if success:
        print("✅ Bucket operation completed successfully")
    else:
        print("❌ Bucket operation failed")
