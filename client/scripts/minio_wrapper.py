#!/usr/bin/env python3
import os
from minio import Minio
from minio.error import S3Error

class MinioWrapper:
    """A wrapper class for Minio client operations."""
    
    def __init__(self, endpoint=None, access_key=None, secret_key=None, secure=False, bucket_name="demo-bucket"):
        """
        Initialize MinIO client with provided configuration.
        
        Args:
            endpoint (str): MinIO server endpoint
            access_key (str): Access key for authentication
            secret_key (str): Secret key for authentication
            secure (bool): Use HTTPS if True, HTTP if False
            bucket_name (str): Default bucket name to use
        """
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        
        # Initialize MinIO client
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        # Ensure bucket exists
        self.ensure_bucket()
    
    def ensure_bucket(self):
        """Create the bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully")
            else:
                print(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")
            raise
    
    def upload_file(self, file_path, object_name=None):
        """
        Upload a file to MinIO server.
        
        Args:
            file_path (str): Path to the local file
            object_name (str, optional): Name of the object in MinIO. If None, uses the filename.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            return False
        
        # Use filename as object_name if not specified
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            # Upload the file
            self.client.fput_object(
                self.bucket_name, object_name, file_path,
            )
            print(f"Successfully uploaded {file_path} as {object_name} to {self.endpoint}")
            return True
        except S3Error as e:
            print(f"Error uploading file to {self.endpoint}: {e}")
            return False
    
    def download_file(self, object_name, file_path=None):
        """
        Download a file from MinIO server.
        
        Args:
            object_name (str): Name of the object in MinIO
            file_path (str, optional): Path where to save the file. If None, saves to current directory.
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Use object_name as local filename if not specified
        if file_path is None:
            file_path = object_name
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        
        try:
            # Download the file
            self.client.fget_object(
                self.bucket_name, object_name, file_path
            )
            print(f"Successfully downloaded {object_name} to {file_path} from {self.endpoint}")
            return True
        except S3Error as e:
            print(f"Error downloading file from {self.endpoint}: {e}")
            return False
    
    def list_objects(self):
        """
        List all objects in the bucket.
        
        Returns:
            list: List of object names in the bucket
        """
        try:
            objects = self.client.list_objects(self.bucket_name, recursive=True)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"Error listing objects: {e}")
            return []
