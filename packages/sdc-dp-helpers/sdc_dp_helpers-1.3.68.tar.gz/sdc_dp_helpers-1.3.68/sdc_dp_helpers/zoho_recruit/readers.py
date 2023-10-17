"""READER FILE FOR ZOHO RECRUIT"""
# pylint: disable=wrong-import-order,arguments-differ, broad-except, too-few-public-methods

from datetime import datetime
from typing import List, Dict, Union, Any, Generator

from sdc_dp_helpers.base_readers import APIRequestsSessionsReader
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import date_string_handler
from sdc_dp_helpers.zoho_recruit.zoho_recruit_sdk import ZohoRecruitAPI


class ZohoRecruitReader(APIRequestsSessionsReader):
    """Zoho Recruit Reader Class

    Args:
        BaseReader (_type_): API Reader Class
    """

    def __init__(self, secrets_filepath: str, config_filepath: str):
        self.configs: Dict[Any, Any] = load_file(config_filepath)
        self.secrets: Dict[Any, Any] = load_file(secrets_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        handler_factory = ZohoRecruitAPI(session=self.sessions, secrets=self.secrets)
        return handler_factory.get_end_point_handler(
            end_point=self.configs["end_point"],
        )

    def _query_handler(
        self, configs: Dict[Any, Any]
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Method ot get the endpoint handler to use

        Args:
            config (Dict[Any, Any]): configs passed to the API endpoint handler

        Returns:
            List[Dict[Any, Any]]:  A list of dictionary of each response
        """
        results = self.service.fetch_data(configs=configs)
        for result in results:
            if result["data"]:
                yield {
                    "data": result["data"],
                    "module": result["module"],
                    "start_page": result["start_page"],
                    "end_point": self.configs["end_point"],
                    "date": datetime.now().date().strftime("%Y%m%d"),
                }
                self.is_success()
            else:
                self.not_success()

    def run_query(
        self,
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Method to run the query"""
        modified_since = self.configs.get("modified_since")
        if modified_since is None:
            modified_since = "50_years_ago"
        modified_since = date_string_handler(modified_since)
        modified_since = datetime.strftime(modified_since, "%Y-%m-%dT%H:%M:%S+00:00")

        self.configs["modified_since"] = modified_since
        results = self._query_handler(configs=self.configs)

        yield from results
