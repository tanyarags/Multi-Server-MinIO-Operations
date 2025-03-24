#!/usr/bin/env python3
"""
MinIO Demo Script - Demonstrates the usage of MinIO wrapper
"""

import os
import json
import pandas as pd
from datetime import datetime
from minio_wrapper import MinioWrapper

def create_sample_files():
    """Create some sample files for the demo"""
    # Text file
    with open("text_sample.txt", "w") as f:
        f.write("This is a sample text file for the MinIO demo.\n")
        f.write("It contains multiple lines of text.\n")
        f.write(f"Created at: {datetime.now().isoformat()}")
    
    # JSON file
    data = {
        "name": "MinIO Demo",
        "version": "1.0.0",
        "features": ["Upload", "Download", "List", "Delete"],
        "timestamp": datetime.now().isoformat()
    }
    with open("data_sample.json", "w") as f:
        json.dump(data, f, indent=4)
    
    # CSV file
    df = pd.DataFrame({
        "id": range(1, 6),
        "name": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
        "value": [10.5, 20.7, 30.9, 40.1, 50.3],
        "active": [True, False, True, True, False]
    })
    df.to_csv("data_sample.csv", index=False)
    
    print("Sample files created successfully.")

def run_demo():
    """Run the MinIO demonstration"""
    # Initialize MinIO wrapper
    minio = MinioWrapper("minio_config.ini")
    
    # Create sample files
    create_sample_files()
    
    print("\n===== MinIO Demo =====\n")
    
    # Upload files
    print("Uploading files...")
    minio.upload_file("text_sample.txt")
    minio.upload_file("data_sample.json")
    minio.upload_file("data_sample.csv")
    
    # Upload data directly
    print("\nUploading data directly...")
    minio.upload_data("This is directly uploaded data", "direct_upload.txt")
    
    # Creating a folder structure
    print("\nCreating folder structure...")
    minio.upload_data("", "folder1/")
    minio.upload_file("text_sample.txt", "folder1/text_in_folder.txt")
    minio.upload_file("data_sample.json", "folder1/subfolder/data_in_subfolder.json")
    
    # List all objects
    print("\nListing all objects:")
    objects = minio.list_objects()
    for obj in objects:
        print(f"  - {obj}")
    
    # List objects in a folder
    print("\nListing objects in folder1:")
    folder_objects = minio.list_objects(prefix="folder1/")
    for obj in folder_objects:
        print(f"  - {obj}")
    
    # Download files
    print("\nDownloading files...")
    minio.download_file("text_sample.txt", "downloaded_text.txt")
    minio.download_file("data_sample.json", "downloaded_data.json")
    
    # Reading downloaded JSON
    print("\nReading downloaded JSON:")
    with open("downloaded_data.json", "r") as f:
        json_data = json.load(f)
        print(f"  - Name: {json_data['name']}")
        print(f"  - Features: {', '.join(json_data['features'])}")
    
    # Download as data
    print("\nDownloading as data:")
    data = minio.download_data("direct_upload.txt")
    if data:
        print(f"  - Content: {data.decode('utf-8')}")
    
    # Delete some objects
    print("\nDeleting objects...")
    minio.delete_object("direct_upload.txt")
    
    # Final list
    print("\nFinal list of objects:")
    final_objects = minio.list_objects()
    for obj in final_objects:
        print(f"  - {obj}")
    
    print("\n===== Demo Complete =====")
    
    # Clean up local files
    print("\nCleaning up local files...")
    os.remove("text_sample.txt")
    os.remove("data_sample.json")
    os.remove("data_sample.csv")
    os.remove("downloaded_text.txt")
    os.remove("downloaded_data.json")
    
    print("Local cleanup complete.")


if __name__ == "__main__":
    run_demo()
