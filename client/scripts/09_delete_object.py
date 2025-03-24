#!/usr/bin/env python3
"""
Script 9: Delete an object from MinIO

This script demonstrates how to:
1. List objects in a bucket
2. Delete a specific object
3. Verify the object was deleted
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

def delete_object():
    """Delete an object from MinIO"""
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
            logger.error(f"Bucket '{bucket_name}' is empty")
            print(f"\nBucket '{bucket_name}' is empty. Please upload some files first.")
            return False
        
        # Print objects before deletion
        print("\nObjects in bucket before deletion:")
        for idx, obj in enumerate(objects, start=1):
            print(f"{idx}. {obj.object_name} ({obj.size} bytes)")
        
        # Find the 'metadata_demo.txt' object if it exists
        target_object = None
        for obj in objects:
            if obj.object_name == "metadata_demo.txt":
                target_object = obj.object_name
                break
        
        # If metadata_demo.txt is not found, use the first object
        if target_object is None:
            target_object = objects[0].object_name
        
        # Confirm deletion
        print(f"\nDeleting object: {target_object}")
        
        # Delete the object
        logger.info(f"Deleting object: {target_object}")
        client.remove_object(bucket_name, target_object)
        
        # List objects after deletion to verify
        updated_objects = list(client.list_objects(bucket_name, recursive=True))
        
        # Check if the object was deleted
        deleted = True
        for obj in updated_objects:
            if obj.object_name == target_object:
                deleted = False
                logger.error(f"Object '{target_object}' was not deleted")
                break
        
        if deleted:
            logger.info(f"Object '{target_object}' was successfully deleted")
            
            # Print objects after deletion
            print("\nObjects in bucket after deletion:")
            if updated_objects:
                for idx, obj in enumerate(updated_objects, start=1):
                    print(f"{idx}. {obj.object_name} ({obj.size} bytes)")
            else:
                print("No objects remaining in bucket")
                
            return True
        else:
            return False
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Deleting an Object ===")
    success = delete_object()
    print("=" * 40)
    if success:
        print("✅ Object deletion completed successfully")
    else:
        print("❌ Object deletion failed")
