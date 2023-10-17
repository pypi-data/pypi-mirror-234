"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import json
import boto3


class SFTPWriter:
    """SFTPWriter Class"""

    def __init__(self, bucket, folder_path, profile_name=None):
        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)
        self.s3_resource = self.boto3_session.resource("s3")
        self.bucket = bucket
        self.folder_path = folder_path

    def write_to_s3(self, payload):
        """
        Writes json to specified s3 location.
        """

        data = json.dumps(payload['data']).encode('utf-8')
        dir_var = payload['dir_var']
        date = payload['date']

        write_path = f"{self.folder_path}/{date}/{dir_var}.json"
        print(f"Writing data to s3://{self.bucket}/{write_path}")
        self.s3_resource.Object(self.bucket, write_path).put(Body=data)
