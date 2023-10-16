import boto3
import json


class AwsClient:
    def get_s3_client(self):
        """
        returns the s3 client
        """
        return S3Handler()


class S3Handler(AwsClient):
    """
    This class handles the S3 file upload/download
    """

    def __init__(self):
        """
        Initialize the S3 file handler
        """
        self.s3 = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")

    def get_json_from_s3(self, bucket, remote_file_path):
        """
        This function will return the json file
        """
        content_object = self.s3_resource.Object(bucket, remote_file_path)
        file_content = content_object.get()["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)
        return json_content
