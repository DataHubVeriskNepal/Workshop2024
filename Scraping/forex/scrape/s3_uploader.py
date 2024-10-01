import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

class S3Uploader:
    def __init__(self):
        self.bucket_name = os.getenv('S3_BUCKET_NAME')  # Set your bucket name
        self.s3 = boto3.client('s3')

    def upload_file(self, local_file, s3_file):
        try:
            self.s3.upload_file(local_file, self.bucket_name, s3_file)
            print(f"File '{local_file}' successfully uploaded to '{self.bucket_name}/{s3_file}'")
        except FileNotFoundError:
            print(f"The file {local_file} was not found")
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            print(f"Failed to upload {local_file} to {self.bucket_name}: {e}")
