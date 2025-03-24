#!/usr/bin/env python3
"""
Script 5: Create folder structure in MinIO

This script demonstrates how to:
1. Create folder-like structure in MinIO
2. Upload files to different "folders"
3. List objects with prefixes
"""

import os
import sys
import json
import logging
from datetime import datetime
from io import BytesIO
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

def create_sample_files():
    """Create sample files for different folders"""
    # Create demo_files directory if it doesn't exist
    os.makedirs("../demo_files", exist_ok=True)
    
    files = {
        "folder1_file.txt": "This is a file that will be stored in folder1/",
        "folder1/subfolder_file.txt": "This is a file that will be stored in folder1/subfolder/",
        "folder2_file.txt": "This is a file that will be stored in folder2/"
    }
    
    created_files = []
    for filename, content in files.items():
        # Ensure the directory exists
        dirname = os.path.dirname(os.path.join("../demo_files", filename))
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        # Create the file
        filepath = os.path.join("../demo_files", filename)
        with open(filepath, "w") as f:
            f.write(content + "\n")
            f.write(f"Created at: {datetime.now().isoformat()}\n")
        
        created_files.append(filepath)
        logger.info(f"Created sample file: {filepath}")
    
    return created_files

def create_folder_structure():
    """Create folder-like structure in MinIO"""
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
        
        # Create sample files
        files = create_sample_files()
        
        # Create "folder" structure by uploading objects with specific prefixes
        # In S3/MinIO, folders don't really exist - they are just prefixes in object names
        
        # 1. Create an empty object with a trailing slash to simulate a folder
        logger.info("Creating 'folder1/' directory marker")
        client.put_object(bucket_name, "folder1/", BytesIO(b""), 0)
        
        logger.info("Creating 'folder2/' directory marker")
        client.put_object(bucket_name, "folder2/", BytesIO(b""), 0)
        
        logger.info("Creating 'folder1/subfolder/' directory marker")
        client.put_object(bucket_name, "folder1/subfolder/", BytesIO(b""), 0)
        
        # 2. Upload files to different folders
        for file_path in files:
            # Generate the object name by removing the '../demo_files/' prefix
            object_name = file_path.replace("../demo_files/", "")
            
            if "folder1/subfolder" in object_name:
                # For the subfolder file, adjust the object name
                dest_obj_name = "folder1/subfolder/" + os.path.basename(object_name)
                logger.info(f"Uploading {file_path} to {dest_obj_name}")
                client.fput_object(bucket_name, dest_obj_name, file_path)
            elif "folder1" in object_name:
                # For the folder1 file
                dest_obj_name = "folder1/" + os.path.basename(object_name)
                logger.info(f"Uploading {file_path} to {dest_obj_name}")
                client.fput_object(bucket_name, dest_obj_name, file_path)
            elif "folder2" in object_name:
                # For the folder2 file
                dest_obj_name = "folder2/" + os.path.basename(object_name)
                logger.info(f"Uploading {file_path} to {dest_obj_name}")
                client.fput_object(bucket_name, dest_obj_name, file_path)
        
        # 3. List objects to show folder structure
        print("\nFolder structure in bucket:")
        print("=" * 40)
        
        # Root level
        print("\nRoot level objects:")
        objects = list(client.list_objects(bucket_name, recursive=False))
        for obj in objects:
            print(f"- {obj.object_name}")
        
        # folder1 level
        print("\nObjects in folder1/:")
        objects = list(client.list_objects(bucket_name, prefix="folder1/", recursive=False))
        for obj in objects:
            print(f"- {obj.object_name}")
        
        # folder1/subfolder level
        print("\nObjects in folder1/subfolder/:")
        objects = list(client.list_objects(bucket_name, prefix="folder1/subfolder/", recursive=False))
        for obj in objects:
            print(f"- {obj.object_name}")
        
        # folder2 level
        print("\nObjects in folder2/:")
        objects = list(client.list_objects(bucket_name, prefix="folder2/", recursive=False))
        for obj in objects:
            print(f"- {obj.object_name}")
        
        # All objects recursively
        print("\nAll objects (recursive):")
        objects = list(client.list_objects(bucket_name, recursive=True))
        for obj in objects:
            print(f"- {obj.object_name}")
        
        return True
        
    except S3Error as e:
        logger.error(f"Error occurred: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Creating Folder Structure ===")
    success = create_folder_structure()
    print("=" * 40)
    if success:
        print("✅ Folder structure created successfully")
    else:
        print("❌ Folder structure creation failed")
