from minio import Minio
from minio.error import S3Error

class MinIO:
    def __init__(self, access_key, secret_key, endpoint):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint
        self.client = Minio(endpoint=endpoint, 
                            access_key=access_key, 
                            secret_key=secret_key)
        
    def upload_file(self, source_file, bucket_name, destination_file):
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")
            
        # Upload the file, renaming it in the process
        self.client.fput_object(
            bucket_name, destination_file, source_file,
        )
        print(
            source_file, "successfully uploaded as object",
            destination_file, "to bucket", bucket_name,
        )    
        
    def get_download_link(self, bucket_name, object_name):
        try:
            # Generate a pre-signed URL for downloading the object
            url = self.client.presigned_get_object(bucket_name, object_name)
            return url
        except S3Error as err:
            print(err)
            return None