"""READER FILE FOR ZOHO RECRUIT"""
# pylint: disable=wrong-import-order,arguments-differ, broad-except, too-few-public-methods

from datetime import datetime
from typing import List, Dict, Union, Any, Generator

from sdc_dp_helpers.base_readers import BaseReader
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.zoho_crm.zoho_crm_sdk import ZohoCRMAPI


class ZohoCRMReader(BaseReader):
    """Zoho CRMReader Class

    Args:
        BaseReader (_type_): API Reader Class
    """

    def __init__(self, creds_filepath: str, config_filepath: str):
        self.configs: Dict[Any, Any] = load_file(config_filepath)
        self.creds: Dict[Any, Any] = load_file(creds_filepath)
        self.service = self._get_auth()
        self.success: List[bool] = []

    def _get_auth(self):
        """Authenticate the service"""

        service = ZohoCRMAPI(creds=self.creds, configs=self.configs)
        return service

    def _query_handler(
        self,
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Method ot get the endpoint handler to use

        Args:
            config (Dict[Any, Any]): configs passed to the API endpoint handler

        Returns:
            List[Dict[Any, Any]]:  A list of dictionary of each response
        """
        results = self.service.fetch_data()
        for result in results:
            if result["data"]:
                yield {
                    "data": result["data"],
                    "module_partition": result["module_partition"],
                    "partition_counter": result["partition_counter"],
                    "date": datetime.now().strftime("%Y%m%d"),
                }
                self.is_success()
            else:
                self.not_success()

    def run_query(
        self,
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Method to run the query"""
        results = self._query_handler()

        yield from results
