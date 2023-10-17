"""MODULE FOR ONESIGNAL"""
# pylint: disable=arguments-differ, too-few-public-methods
import sys
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.base_readers import BaseReader
from sdc_dp_helpers.onesignal.onesignal_sdk import OneSignalHandlerFactory


class OneSignalReader(BaseReader):
    """reader for one signal"""

    def __init__(self, creds_filepath: str, config_filepath: str):
        self.creds: dict = load_file(creds_filepath)
        self.configs: dict = load_file(config_filepath)
        self.service = self._get_auth()

    def _get_auth(self):
        """class method to acquire the onesignal api sdk service"""
        handler_factory = OneSignalHandlerFactory()
        return handler_factory.get_endpoint_handler(
            creds=self.creds, configs=self.configs
        )

    def _query_handler(self):
        """make api call to endpoint"""
        yield from self.service.fetch_data()

    def run_query(self):
        """main loop for the reader"""
        results = self._query_handler()
        if not results:
            self.not_success()
            print(
                f"No data got for {self.configs['endpoint']} for {self.creds['app_id']}"
            )
            sys.exit()
        for result in results:
            self.is_success()
            yield {"date": result["date"], "data": result["data"]}
