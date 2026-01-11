from fastapi import UploadFile
import boto3


class S3Storage:
    def __init__(self):
        self.PUBLIC_URL = 'https://pub-f0b804e4a87c49ec9fa377abd59b7d70.r2.dev'
        self.BUCKET_NAME = 'group04092025'

    def get_s3_client(self):

        ACCESS_KEY = 'e13de50095d962888c357d437d0bc855'
        SECRET_KEY = '92c703ef97a891d9dc79f3adb3ed484b18eacc6f9b3d5fb0c4bbe6f586d31c2e'
        ENDPOINT = "https://8721af4803f2c3c631a90d8b64d397b7.r2.cloudflarestorage.com"
        REGION_NAME = 'EEUR'

        s3client = boto3.client(
            service_name='s3',
            region_name=REGION_NAME,
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        return s3client

    def upload_file(self, file: UploadFile, product_uuid: str) -> str:
        s3_client = self.get_s3_client()
        target_file_name = f"products/{product_uuid}/{file.filename}"
        s3_client.upload_fileobj(file.file, self.BUCKET_NAME, target_file_name)
        return F'{self.PUBLIC_URL}/{target_file_name}'


s3_service = S3Storage()