# MinIO Demo Scripts

This directory contains a collection of demonstration scripts to show various MinIO operations in a step-by-step manner.

## Script Overview

1. **01_create_bucket.py** - Create a new bucket in MinIO
2. **02_upload_file.py** - Upload a file to the bucket
3. **03_list_objects.py** - List all objects in the bucket
4. **04_download_file.py** - Download a file from the bucket
5. **05_create_folder_structure.py** - Create folders/prefixes in the bucket
6. **06_delete_local_file.py** - Delete a local file to demonstrate recovery from MinIO
7. **07_recover_file.py** - Recover the deleted file from MinIO
8. **08_object_metadata.py** - Work with object metadata
9. **09_delete_object.py** - Delete an object from the bucket
10. **10_policy_management.py** - Set access policies for the bucket

## Helper Scripts

- **run_demo.sh** - Runs all demo scripts in sequence with pauses between each
- **cleanup.sh** - Cleans up local demo files after completing the demo

## Running the Demo

### Option 1: Run the entire demo sequence

```bash
bash run_demo.sh
```

This will run all scripts in order, pausing between each script for you to review the output.

### Option 2: Run individual scripts

You can run any script individually to demonstrate a specific MinIO operation:

```bash
python 02_upload_file.py
```

### Requirements

These scripts require the following Python packages:
- minio
- configparser
- tabulate (for formatted output in list_objects.py)

## Demo Flow

1. Create a bucket
2. Upload files to the bucket
3. List and explore objects in the bucket
4. Download files from the bucket
5. Create a folder structure (demonstrating prefixes)
6. Simulate data loss by deleting a local file
7. Recover the file from MinIO
8. Work with object metadata
9. Delete objects from the bucket
10. Manage bucket policies

## Tips for Presenters

- Run each script with explanation in between
- Show the MinIO Console UI in parallel to visualize changes
- Emphasize how MinIO uses prefixes to simulate folders
- Highlight the data recovery scenario (scripts 6-7) to demonstrate data durability
- Use the policy management script to explain access control
