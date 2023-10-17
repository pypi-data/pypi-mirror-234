"""SDK MODULE FOR ONESIGNAL"""
# pylint: disable=arguments-differ,too-few-public-methods
import os
import sys
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Generator
from datetime import datetime
import requests
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler
from sdc_dp_helpers.api_utilities.file_managers import parse_zip_to_csv


class AuthenticationError(Exception):
    """class for Authentication Errors"""


class NoDownloadYetError(Exception):
    """class for handling no download ready yet"""


class ExistingScheduledDownloadError(Exception):
    """Error raised if there exists a scheduled download"""


class CSVExportCreationError(Exception):
    """Error raised when we fail to create bulk job and get back a None"""


class ViewNotificationsDownloadError(Exception):
    """Error for view notifications data download"""


class APICallHandler(ABC):
    """Base class for API Calls"""

    def __init__(self, creds: dict):
        self.creds = creds
        self._header = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Basic {self.creds['api_key']}",
            "User-Agent": "Mozilla/5.0",
        }

    @abstractmethod
    def api_call(self, **kwargs):
        """_summary_
        Raises:
            NotImplementedError: needs to be implemented for all child classes
        """
        raise NotImplementedError


class CreateBulkDownload(APICallHandler):
    """Class for Creating Bulk Doanload"""

    @retry_handler(ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2)
    @retry_handler(
        ExistingScheduledDownloadError, total_tries=10, initial_wait=2, backoff_factor=2
    )
    def api_call(self, session: requests.Session) -> Dict[str, str]:
        _app_id: str = self.creds["app_id"]
        url = f"https://onesignal.com/api/v1/players/csv_export?app_id={_app_id}"
        try:
            response = session.post(url=url, headers=self._header, timeout=61)
            response.raise_for_status()
            return response.json()

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ConnectTimeout,
        ) as exc:
            raise ConnectionError(exc) from exc
        except requests.exceptions.RequestException as exc:
            if "Please include a case-sensitive header of Authorization" in str(
                response.json()
            ):
                raise AuthenticationError(
                    "Please check the credentials used to make api call"
                ) from exc
            if "User already running another CSV export." in str(response.json()):
                print("Got into the down scheduled part")
                raise ExistingScheduledDownloadError(response.json()) from exc

            raise exc


class FetchBulkDownload(APICallHandler):
    """Class to fetch the generated bulk download"""

    # we wait maximum 30 minutes for download to be ready otherwise we just raise an error
    @retry_handler(NoDownloadYetError, total_tries=10, initial_wait=2, backoff_factor=2)
    @retry_handler(ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2)
    def api_call(self, session: requests.Session, url: str):
        """call for downloading the prepared csv export"""
        try:
            response = session.get(url=url, timeout=61)
            response.raise_for_status()
            return response.content
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ConnectTimeout,
        ) as exc:
            raise ConnectionError(exc) from exc
        except requests.exceptions.RequestException as exc:
            if response.status_code == 404:
                raise NoDownloadYetError(exc) from exc
            raise exc


class ViewNotificationsDownload(APICallHandler):
    """class for fetching view notifications"""

    @retry_handler(ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 5)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def api_call(
        self, session: requests.Session, limit: int, offset: int
    ) -> Tuple[bool, Dict[Any, Any]]:
        """
        Handles the view notification request attempt.
        """
        _app_id: str = self.creds["app_id"]
        url = f"https://onesignal.com/api/v1/notifications?app_id={_app_id}"
        more_records = False
        try:
            response = session.get(
                url=url,
                headers=self._header,
                params={"limit": limit, "total_count": "true", "offset": offset},
                timeout=61,
            )
            response.raise_for_status()
            results = response.json()
            total_records: int = int(results.get("total_count", 0))
            if total_records >= offset:
                more_records = True

            return more_records, results
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ConnectTimeout,
        ) as exc:
            raise ConnectionError(exc) from exc
        except requests.exceptions.RequestException as exc:
            if "Please include a case-sensitive header of Authorization" in str(
                response.json()
            ):
                raise AuthenticationError(
                    "Please check the credentials used to make api call"
                ) from exc
            raise exc


class OneSignalHandler:
    """class to do the data pull"""

    def __init__(self, creds: dict, configs: dict):
        self.creds = creds
        self.session = requests.Session()
        self.configs = configs
        self.file_size_limit: int = self.configs.get("file_size_limit", 500000)

    def fetch_data(self) -> Generator[Dict[Any, Any], None, None]:
        """Method to fetch the data from source"""
        raise NotImplementedError


class ViewNotificationsHandler(OneSignalHandler):
    """Fetch View Notifications"""

    def fetch_data(self):
        """fecth data method"""
        # gather data per offset given the set of limits
        offset: int = 0
        limit = self.configs.get("limit", 50)
        api_call_handler: APICallHandler = ViewNotificationsDownload(creds=self.creds)
        more_records = True
        result_array: List[Dict[Any, Any]] = []
        partition_dataset: Dict[Any, Any] = {}
        while more_records:
            response = api_call_handler.api_call(
                session=self.session, limit=limit, offset=offset
            )
            if response is None:
                raise ViewNotificationsDownloadError("No data for view notifications")
            more_records, results = response[0], response[1]
            notifications = results.get("notifications")
            if notifications is not None and isinstance(notifications, list):
                print(f"At offset {offset} of {results.get('total_count')}.")
                result_array.extend(notifications)

            offset += limit

        if not result_array:
            print("No view notifications data")
            sys.exit()

        for result in result_array:
            date_value = result.get("completed_at")
            if date_value is not None:
                date_value = datetime.fromtimestamp(int(date_value)).strftime("%Y%m%d")
                result["completed_at_date"] = date_value
                partition_dataset.setdefault(date_value, []).append(result)

        for date, date_dataset in partition_dataset.items():
            yield {"date": date, "data": date_dataset}


class CSVExportHandler(OneSignalHandler):
    """Class to make the CSV Export Job"""

    @staticmethod
    def add_created_at_date(row) -> Dict[Any, Any]:
        """function to add created_at_date"""
        try:
            row["created_at_date"] = str(
                datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").date()
            ).replace("-", "")
        except ValueError:
            row["created_at_date"] = str(
                datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S.%f").date()
            ).replace("-", "")
        return row

    def fetch_data(self):
        """fetch data method for csv export"""
        bulk_creator: APICallHandler = CreateBulkDownload(creds=self.creds)
        api_call_handler: APICallHandler = FetchBulkDownload(creds=self.creds)
        bulk_job: Dict[str, str] = bulk_creator.api_call(self.session)
        if (bulk_job is None) or not isinstance(bulk_job, dict):
            raise CSVExportCreationError(
                f"Failed to create bulk job for {self.creds['app_id']}"
            )
        csv_file_url = bulk_job.get("csv_file_url")
        if csv_file_url is not None and isinstance(csv_file_url, str):
            print(f"created_job app_id: {self.creds['app_id']}: {bulk_job}")
            response = api_call_handler.api_call(self.session, url=csv_file_url)
            partition_dataset: Dict[Any, Any] = {}
            results = parse_zip_to_csv(response=response, file_type="gzip")
            if not results:
                print(f"No data for csv export for appi_id {self.creds['app_id']}")
                sys.exit()
            for result in results:
                result = self.add_created_at_date(result)  # add created_at_date
                date_value = result.get("created_at_date")
                if date_value is not None:
                    partition_dataset.setdefault(date_value, []).append(result)

            for date, date_dataset in partition_dataset.items():
                yield {"date": date, "data": date_dataset}


class OneSignalHandlerFactory:
    """Factory to get us the Handler"""

    def get_endpoint_handler(self, creds: dict, configs: dict) -> OneSignalHandler:
        """Gets Us the Endpoint Hanlder to Use"""
        endpoint_handlers = {
            "csv_export": CSVExportHandler,
            "view_notifications": ViewNotificationsHandler,
        }

        return endpoint_handlers[configs["endpoint"]](creds=creds, configs=configs)
