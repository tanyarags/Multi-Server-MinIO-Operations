#!/usr/bin/env python3
"""
Script 3: List objects in a MinIO bucket

This script demonstrates how to:
1. Connect to a MinIO server
2. List all objects in a bucket
3. Display their properties
"""

import sys
import logging
from tabulate import tabulate
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

def list_objects():
    """List all objects in a MinIO bucket"""
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
        
        # List all objects
        objects = list(client.list_objects(bucket_name, recursive=True))
        
        if not objects:
            logger.info(f"Bucket '{bucket_name}' is empty")
            print(f"\nBucket '{bucket_name}' is empty. Please upload some files first.")
            return True
        
        # Format the object list for display
        table_data = []
        for obj in objects:
            # Calculate size in a readable format
            size = obj.size
            size_str = None
            
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024**2:
                size_str = f"{size/1024:.2f} KB"
            elif size < 1024**3:
                size_str = f"{size/1024**2:.2f} MB"
            else:
                size_str = f"{size/1024**3:.2f} GB"
                
            # Format the last modified date
            if hasattr(obj, 'last_modified'):
                last_modified = obj.last_modified.strftime("%Y-%m-%d %H:%M:%S")
            else:
                last_modified = "Unknown"
                
            table_data.append([
                obj.object_name,
                size_str,
                last_modified,
                obj.etag.replace('"', '')
            ])
        
        # Print the table
        headers = ["Object Name", "Size", "Last Modified", "ETag"]
        print("\nObjects in bucket:", bucket_name)
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        logger.info(f"Found {len(objects)} objects in bucket '{bucket_name}'")
        
        return True
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # try:
    #     # Try to import tabulate, install if not available
    #     import tabulate
    # except ImportError:
    #     print("The 'tabulate' package is required for this script.")
    #     print("Installing tabulate...")
    #     import subprocess
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    #     import tabulate
    
    print("=== MinIO Demo: Listing Objects ===")
    success = list_objects()
    print("=" * 40)
    if success:
        print("✅ Object listing completed successfully")
    else:
        print("❌ Object listing failed")
