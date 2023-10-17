"""
    CUSTOM FALCON READER CLASSES
"""
# pylint: disable=too-few-public-methods,import-error,unused-import,too-many-locals,arguments-differ

from typing import Generator, List, Dict
from datetime import datetime

import requests

from sdc_dp_helpers.base_readers import BaseReader
from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.falcon.falcon_sdk import FalconAPICall, FalconQuotaException


class FalconReader(BaseReader):
    """Falcon Reader class

    Args:
        BaseReader (_type_): API Reader Class
    """

    def __init__(self, creds_file: str, config_file=None):
        """creds_file has crecdentials config_file has api pull configs"""
        self._creds: dict = load_file(creds_file, "yml")
        self._config: dict = load_file(config_file, "yml")
        self.session: requests.Session = requests.Session()
        self.success = []
        self.service: FalconAPICall = self._get_auth()
        self.start = 0

    def _get_auth(self):
        self.service = FalconAPICall(
            session=self.session, creds=self._creds, config=self._config
        )

        return self.service

    def _query_handler(
        self, start_date: str, end_date: str, network: str, channel_ids: dict
    ) -> List[Dict]:

        data = self.service.get_data(
            start_date=start_date,
            end_date=end_date,
            network=network,
            channel_ids=channel_ids,
        )
        return data

    def run_query(self) -> Generator:
        """Calls the Query Handler"""
        endpoint_name = self._config.get("endpoint_name")
        channel_ids = self.service.get_channel_ids()
        network = self._config["networks"]

        date_iterator = date_range_iterator(
            start_date=self._config["since"],
            end_date=self._config["until"],
            interval="1_day",
            end_inclusive=False,
            time_format="%Y-%m-%dT00:00:00Z",
        )
        try:
            for start_date, end_date in date_iterator:
                payload: List = []
                payload = self._query_handler(
                    start_date=start_date,
                    end_date=end_date,
                    network=network,
                    channel_ids=channel_ids,
                )
                date = datetime.strftime(datetime.strptime(
                    start_date, "%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%d")
                if payload:
                    yield {
                        "networks": network,
                        "date": date,
                        "data": payload,
                    }
                    self.start = 0
                    self.is_success()
                else:
                    self.not_success()
                    print(
                        f"No data for endpoint {endpoint_name} for date : {date}")
        except FalconQuotaException as exp:
            raise exp
