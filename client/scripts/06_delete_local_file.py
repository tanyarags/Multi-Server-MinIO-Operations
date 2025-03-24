#!/usr/bin/env python3
"""
Script 6: Delete a local file to simulate data loss

This script demonstrates how to:
1. List downloaded files
2. Delete a local file
3. Verify the file is no longer available locally
"""

import os
import sys
import glob
import logging
from datetime import datetime

# Add parent directory to path to import the wrapper
sys.path.append('..')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def delete_local_file():
    """Delete a local downloaded file to simulate data loss"""
    try:
        # Check for downloaded files
        download_dir = "../demo_files/downloads"
        if not os.path.exists(download_dir):
            logger.error(f"Download directory '{download_dir}' does not exist")
            print("\nPlease run script 04_download_file.py first to download files")
            return False
        
        # Find all files in the downloads directory
        files = glob.glob(os.path.join(download_dir, "**"), recursive=True)
        
        # Filter to only get files, not directories
        files = [f for f in files if os.path.isfile(f)]
        
        if not files:
            logger.error(f"No files found in directory '{download_dir}'")
            print("\nPlease run script 04_download_file.py first to download files")
            return False
        
        # Print list of files before deletion
        print("\nFiles in downloads directory before deletion:")
        for idx, file_path in enumerate(files, start=1):
            file_size = os.path.getsize(file_path)
            print(f"{idx}. {os.path.basename(file_path)} ({file_size} bytes)")
        
        # For simplicity, delete the first file
        # In a real application, you might want to let the user choose
        file_to_delete = files[0]
        
        # Confirm deletion
        print(f"\nSimulating data loss by deleting: {file_to_delete}")
        
        # Keep backup before deletion (in a real scenario, we wouldn't have this)
        backup_dir = "../demo_files/backup"
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, os.path.basename(file_to_delete))
        
        # Note: In a real data loss scenario, you wouldn't make a backup
        # This is just for the demo to be reversible
        with open(file_to_delete, 'rb') as src, open(backup_file, 'wb') as dst:
            dst.write(src.read())
        logger.info(f"Created backup at {backup_file} (just for the demo)")
        
        # Delete the file
        logger.info(f"Deleting {file_to_delete}")
        os.remove(file_to_delete)
        logger.info(f"File deleted: {file_to_delete}")
        
        # Verify file is gone
        if not os.path.exists(file_to_delete):
            logger.info(f"Verified: File no longer exists at {file_to_delete}")
            
            # Print list of files after deletion
            remaining_files = glob.glob(os.path.join(download_dir, "**"), recursive=True)
            remaining_files = [f for f in remaining_files if os.path.isfile(f)]
            
            print("\nFiles in downloads directory after deletion:")
            if remaining_files:
                for idx, file_path in enumerate(remaining_files, start=1):
                    file_size = os.path.getsize(file_path)
                    print(f"{idx}. {os.path.basename(file_path)} ({file_size} bytes)")
            else:
                print("No files remaining in downloads directory")
            
            # Store the name of the deleted file for the next script
            with open("../demo_files/deleted_file_info.txt", "w") as f:
                f.write(file_to_delete)
            logger.info(f"Stored deleted file info for recovery demo")
            
            return True
        else:
            logger.error(f"Failed to delete file: {file_to_delete}")
            return False
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("=== MinIO Demo: Deleting Local File (Simulating Data Loss) ===")
    success = delete_local_file()
    print("=" * 60)
    if success:
        print("✅ File deleted successfully (simulating local data loss)")
        print("\nNow you can run 07_recover_file.py to recover the file from MinIO")
    else:
        print("❌ File deletion failed")