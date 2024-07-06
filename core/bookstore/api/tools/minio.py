from minio import Minio
from minio.error import S3Error
from os import getenv

class MinIO:
    
    def get_client(self):
        try:
            client = Minio(
                endpoint=getenv("MINIO_ENDPOINT"),
                access_key=getenv("MINIO_ACCESS"),
                secret_key=getenv("MINIO_SECRET"),
                secure=False  # Change to True if you're using HTTPS
            )
            return client
        except Exception as e:
            print(f"Failed to create Minio client: {e}")
            raise

    def upload_file(self, bucket_name, destination_file, data, file_size):
        try:
            client = self.get_client()
            found = client.bucket_exists(bucket_name)
            if not found:
                client.make_bucket(bucket_name)
                print("Created bucket", bucket_name)
            else:
                print("Bucket", bucket_name, "already exists")

            client.put_object(
                bucket_name, destination_file, data, file_size
            )
            print(
                "Successfully uploaded as object",
                destination_file, "to bucket", bucket_name,
            )
        except S3Error as e:
            print(f"S3Error occurred: {e}")
            # Optionally, log the error or raise an exception
        except Exception as e:
            print(f"An error occurred: {e}")
            # Optionally, log the error or raise an exception

    def get_download_link(self, bucket_name, object_name):
        try:
            client = self.get_client()
            url = client.presigned_get_object(bucket_name, object_name)
            return url
        except S3Error as e:
            print(f"S3Error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def download_object(self, bucket_name, object_name):
        try:
            client = self.get_client()
            objects = list(client.list_objects(bucket_name, object_name))
            if objects:
                file = client.get_object(bucket_name, object_name)
                return file
            else:
                print(f"No objects found in bucket {bucket_name} with name {object_name}")
                return None
        except S3Error as e:
            print(f"S3Error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
