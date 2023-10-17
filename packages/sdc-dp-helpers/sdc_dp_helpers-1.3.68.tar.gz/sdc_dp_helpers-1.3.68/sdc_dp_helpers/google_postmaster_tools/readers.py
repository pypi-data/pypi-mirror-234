"""
CUSTOM READERS MODULE FOR GOOGLE POSTMASTER READER
"""
from typing import Dict, List, Any, Union, Generator
from googleapiclient import discovery, errors
from google.oauth2 import service_account

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import (
    date_string_handler,
    date_range_iterator,
)
from sdc_dp_helpers.base_readers import BaseReader


class GooglePostmasterReader(BaseReader):
    """
    Google Postmaster Reader
    """

    def __init__(self, creds_filepath: str, config_filepath: str) -> None:
        super().__init__()
        self.secrets: Dict[Any, Any] = load_file(creds_filepath)
        self.config: Dict[Any, Any] = load_file(config_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client.
        """
        service = None
        try:
            credentials = service_account.Credentials.from_service_account_info(
                info=self.secrets,
                scopes=["https://www.googleapis.com/auth/postmaster.readonly"],
            )
            service = discovery.build(
                serviceName="gmailpostmastertools",
                version="v1beta1",
                credentials=credentials,
            )
            if service is None:
                raise RuntimeError("Service is null.")
            if not hasattr(service, "domains"):
                raise KeyError("Service does not have domains atribute.")
        except KeyError as err:
            self.not_success()
            print(f"An error has occurred: {err}")
        except RuntimeError as err:
            self.not_success()
            print(f"An error has occurred: {err}")
        return service

    def _query_handler(self, *args, **kwargs) -> dict:
        # pylint: disable=no-member
        """Handles the Query call"""
        response = None
        if not {"domain", "date"}.issubset(set(kwargs.keys())):
            raise KeyError("Invalid arguments - expecting: domain, date")
        response = (
            self.service.domains()
            .trafficStats()
            .get(name=f"domains/{kwargs['domain']}/trafficStats/{kwargs['date']}")
            .execute()
        )
        if response is None:
            raise RuntimeError("response is 'None'")
        self.is_success()
        return response

    def run_query(
        self,
    ) -> Union[
        Generator[Dict[List[Dict[Any, Any]], Any], None, None],
        Dict[List[Dict[Any, Any]], Any],
    ]:
        """Runs the query"""
        start_date = date_string_handler(self.config["start_date"])
        end_date = date_string_handler(self.config["end_date"])
        print(f" {start_date} {end_date} ")
        if start_date > end_date:
            raise ValueError(
                "An error has occured: "
                + f"- Start Date {start_date}"
                + f"is not before {end_date}."
            )
        if self.service is None:
            raise ValueError("Service is null.")
        domain = self.config["domain"]
        for date, _ in date_range_iterator(
            start_date=start_date,
            end_date=end_date,
            interval="1_day",
            end_inclusive=False,
            time_format="%Y%m%d",
        ):
            try:
                print(f"date : {date}")
                dataset = self._query_handler(domain=domain, date=date)
                yield {
                    "date": date,
                    "brand": domain.replace(".", "_"),
                    "data": [dataset],
                }
            except RuntimeError as err:
                self.not_success()
                print(f"Error occured: {err}")
            except errors.HttpError as err:
                self.not_success()
                print(f"An error occurred: {err}")
            except KeyError as err:
                self.not_success()
                print(f"An error occurred: {err}")
