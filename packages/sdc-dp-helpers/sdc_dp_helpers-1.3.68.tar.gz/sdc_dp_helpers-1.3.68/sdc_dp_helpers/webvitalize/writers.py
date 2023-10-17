"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import json
from datetime import datetime
import boto3


class WebVitalWriter:
    """FTPWriter Class"""

    def __init__(self, bucket, folder_path, profile_name=None):
        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")
        self.bucket = bucket
        self.folder_path = folder_path

    def write_to_s3(self, payload: dict):
        """
        Writes json to specified s3 location.
        """
        data = json.dumps(payload["response"]["data"])
        venture = payload["venture"]
        ts_now = payload["ts_now"]

        write_path = f"{self.folder_path}/{venture}.json"
        print(f"Writing data to s3://{self.bucket}/{write_path}")
        self.s3_resource.Object(self.bucket, write_path).put(Body=data)

        date_partition = datetime.strftime(datetime.fromtimestamp(ts_now), '%Y-%m-%d')

        write_path = f"{self.folder_path}/archive/{date_partition}/{ts_now}.json"
        print(f"Writing archive data to s3://{self.bucket}/{write_path}")
        self.s3_resource.Object(self.bucket, write_path).put(Body=data)
