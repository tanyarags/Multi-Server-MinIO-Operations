#!/bin/bash
# Master script to run the MinIO demo

# Colors for better readability
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}             MinIO Demo Session               ${NC}"
echo -e "${BLUE}===============================================${NC}"
echo

# Function to run a script and wait for user input before continuing
run_script() {
    script=$1
    title=$2
    
    echo -e "${YELLOW}Step: ${title}${NC}"
    echo -e "${YELLOW}----------------------------------------${NC}"
    
    # Check if script exists
    if [ ! -f "$script" ]; then
        echo -e "${RED}Error: Script $script not found!${NC}"
        exit 1
    fi
    
    # Execute the script
    if [[ $script == *.py ]]; then
        python "$script"
    else
        bash "$script"
    fi
    
    echo
    read -p "Press Enter to continue to the next step..."
    echo
}

cd scripts
# Make sure all Python scripts are executable
chmod +x *.py

# Run each script in sequence
run_script "01_create_bucket.py" "Creating a MinIO Bucket"
run_script "02_upload_file.py" "Uploading a File to MinIO"
run_script "03_list_objects.py" "Listing Objects in a Bucket"
run_script "04_download_file.py" "Downloading a File from MinIO"
run_script "05_create_folder_structure.py" "Creating Folder Structure in MinIO"
run_script "06_delete_local_file.py" "Simulating Data Loss (Deleting Local File)"
run_script "07_recover_file.py" "Recovering a Deleted File from MinIO"
run_script "08_object_metadata.py" "Working with Object Metadata"
run_script "09_delete_object.py" "Deleting an Object from MinIO"
#run_script "10_policy_management.py" "Managing Bucket Policies"

echo -e "${GREEN}===============================================${NC}"
echo -e "${GREEN}             Demo Completed!                  ${NC}"
echo -e "${GREEN}===============================================${NC}"
echo
echo "You can clean up the local demo files by running:"
echo "bash cleanup.sh"
echo
echo "Thank you for participating in the MinIO demo!"
