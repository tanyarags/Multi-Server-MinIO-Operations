#!/usr/bin/env python3
"""
MinIO Wrapper - A simple wrapper for MinIO operations with configuration file support
"""

import os
import io
import configparser
from minio import Minio
from minio.error import S3Error

class MinioWrapper:
    """
    A wrapper class for MinIO operations that reads configuration from a file
    and provides simplified read/write operations.
    """
    
    def __init__(self, config_path="minio_config.ini"):
        """
        Initialize the MinIO client using credentials from a config file
        
        Args:
            config_path (str): Path to the configuration file
        """
        # Read configuration file
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        # Extract MinIO connection details
        self.endpoint = self.config['minio']['endpoint']
        self.access_key = self.config['minio']['access_key']
        self.secret_key = self.config['minio']['secret_key']
        self.secure = self.config['minio'].getboolean('secure')
        self.bucket_name = self.config['minio']['bucket_name']
        
        # Initialize MinIO client
        self.client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        
        # Ensure bucket exists
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create the bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully")
            else:
                print(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as err:
            print(f"Error checking/creating bucket: {err}")
    
    def upload_file(self, file_path, object_name=None):
        """
        Upload a file to MinIO
        
        Args:
            file_path (str): Path to the file to upload
            object_name (str, optional): Name to store in MinIO. Defaults to filename.
        
        Returns:
            bool: Success status
        """
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path
            )
            print(f"'{file_path}' successfully uploaded as '{object_name}'")
            return True
        except S3Error as err:
            print(f"Error uploading file: {err}")
            return False
    
    def upload_data(self, data, object_name):
        """
        Upload in-memory data to MinIO
        
        Args:
            data (bytes or str): Data to upload
            object_name (str): Name to store in MinIO
        
        Returns:
            bool: Success status
        """
        try:
            # Convert string to bytes if needed
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Upload data
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=io.BytesIO(data),
                length=len(data)
            )
            print(f"Data successfully uploaded as '{object_name}'")
            return True
        except S3Error as err:
            print(f"Error uploading data: {err}")
            return False
    
    def download_file(self, object_name, file_path=None):
        """
        Download a file from MinIO
        
        Args:
            object_name (str): Name of the object in MinIO
            file_path (str, optional): Path to save the file. Defaults to object_name.
        
        Returns:
            bool: Success status
        """
        if file_path is None:
            file_path = object_name
        
        try:
            self.client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path
            )
            print(f"'{object_name}' successfully downloaded to '{file_path}'")
            return True
        except S3Error as err:
            print(f"Error downloading file: {err}")
            return False
    
    def download_data(self, object_name):
        """
        Download an object from MinIO and return as bytes
        
        Args:
            object_name (str): Name of the object in MinIO
        
        Returns:
            bytes or None: Object data or None if error
        """
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            data = response.read()
            response.close()
            return data
        except S3Error as err:
            print(f"Error downloading data: {err}")
            return None
    
    def list_objects(self, prefix="", recursive=True):
        """
        List objects in the bucket
        
        Args:
            prefix (str, optional): Prefix to filter objects. Defaults to "".
            recursive (bool, optional): Whether to list recursively. Defaults to True.
        
        Returns:
            list: List of object names
        """
        try:
            objects = self.client.list_objects(
                bucket_name=self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            object_list = [obj.object_name for obj in objects]
            return object_list
        except S3Error as err:
            print(f"Error listing objects: {err}")
            return []
    
    def delete_object(self, object_name):
        """
        Delete an object from MinIO
        
        Args:
            object_name (str): Name of the object to delete
        
        Returns:
            bool: Success status
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            print(f"'{object_name}' successfully deleted")
            return True
        except S3Error as err:
            print(f"Error deleting object: {err}")
            return False


# Example usage
if __name__ == "__main__":
    # Initialize client
    minio = MinioWrapper("minio_config.ini")
    
    # Upload a text file
    with open("sample.txt", "w") as f:
        f.write("This is a sample file for MinIO demo")
    
    minio.upload_file("sample.txt")
    
    # Upload data directly
    minio.upload_data("This is some data uploaded directly", "direct_upload.txt")
    
    # List objects
    objects = minio.list_objects()
    print(f"Objects in bucket: {objects}")
    
    # Download a file
    minio.download_file("sample.txt", "sample_downloaded.txt")
    
    # Download as data
    data = minio.download_data("direct_upload.txt")
    if data:
        print(f"Downloaded data: {data.decode('utf-8')}")
    
    # Delete objects
    minio.delete_object("sample.txt")
    minio.delete_object("direct_upload.txt")
