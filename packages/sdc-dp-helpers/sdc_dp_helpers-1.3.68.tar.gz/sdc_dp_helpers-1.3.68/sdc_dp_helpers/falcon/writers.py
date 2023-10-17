# pylint: disable=too-few-public-methods,disable=R0913, disable=C0301

"""
    CUSTOM WRITER CLASSES
"""
import re
import json
from typing import Union, List, Any, Dict, Tuple, Optional
import boto3

from sdc_dp_helpers.base_writers import BaseWriter


class FalconWriter(BaseWriter):
    """WRITER FOR FALCON DATA"""

    def __init__(
        self,
        bucket: str,
        folder_path: str,
        destination: str,
        configs: Optional[Dict[str, Any]] = None,
        clear_destination: bool = False,
    ):
        self.success: List[bool] = []
        self.current_destination: Union[str, None] = None
        self.boto3_session = boto3.Session()
        self.s3_resource = self.boto3_session.resource("s3")
        super().__init__(
            bucket=bucket,
            folder_path=folder_path,
            destination=destination,
            configs=configs,
            clear_destination=clear_destination,
        )

    def verify_data(
        self, payload: Dict[str, Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[str, Any]): expecting a dictionary having data, date and dimension

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
        """
        if not {"data", "date", "networks"}.issubset(set(payload.keys())):
            raise KeyError("Invalid payload expecting: date, data, networks")

        if not payload.get("date"):
            raise ValueError("Date cannot be None")
        if not re.search(r"\d{4}\-\d{2}\-\d{2}", payload["date"]):
            raise ValueError(
                "Invalid date format for partitioning expected: 'YYYY-mm-dd'"
            )
        if not isinstance(payload["data"], list):
            raise TypeError(
                "Invalid data value passed: expected List[Dict, Dict]")
        if not payload["networks"]:
            raise ValueError("Networks can not be None")
        if not isinstance(payload["networks"], str):
            raise TypeError("Invalid networks value passed: expected str")
        _date = payload.get("date").replace("-", "")
        _data: list = payload["data"]
        _networks: str = payload["networks"]
        _write_path: str = f"{self.folder_path}/{_networks}/{_date}"
        return _write_path, _data

    def write_stats_to_s3(
        self,
        stats: str,
        date: str,
        network: str,
        endpoint: str,
        target_table_name: str = "falcon_api_statistics"
    ) -> None:
        """
        Write statistics about the number of api calls on a particular date, network and endpoint.
        """
        write_path: str = f"{target_table_name}/date={date}/endpoint={endpoint}/network={network}/stats.json"
        if stats:
            print(
                f"Writing data to s3://{self.bucket}/{write_path}  \
                partitioned by networks and date."
            )
            self.s3_resource.Object(self.bucket, write_path).put(
                Body=json.dumps(stats))
            self.is_success()
