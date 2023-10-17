"""
    CUSTOM READER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
# pylint: disable=no-member,too-many-locals,broad-except,too-few-public-methods,arguments-differ,line-too-long,broad-exception-raised,inconsistent-return-statements
import os
from datetime import datetime

from google.oauth2 import service_account
from google.cloud import enterpriseknowledgegraph as ekg
from google.protobuf.json_format import MessageToDict

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.data_managers import multiple_regex_replace
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler
from sdc_dp_helpers.base_readers import BaseReader


class GoogleKnowledgeGraphReader(BaseReader):
    """Google Knowledge Graph Class"""

    def __init__(self, secrets_filepath: str, config_filepath: str):
        self.secrets: str = secrets_filepath
        self.config: dict = load_file(config_filepath)
        self.client = self._get_auth()
        self.dataset: list = []
        self.success = []

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client

        """
        credentials = service_account.Credentials.from_service_account_file(self.secrets)
        client = ekg.EnterpriseKnowledgeGraphServiceClient(credentials=credentials)
        return client

    def query_partition(self, query: str, language: str = None) -> str:
        """Helper to get the query partition string
        :query: "string",
        :language:"string"}
        :returns: query_partition - str
        """
        query = query.strip()
        query_partition = multiple_regex_replace(
            query, {".": "_dot_", " ": "_space_", "+": "_plus_"}
        )
        if language:
            query_partition = f"{query_partition}_lang_{language}"

        return query_partition

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 2)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", "0.01"),
    )
    @retry_handler(
        exceptions=ConnectionError,
        total_tries=int(os.environ.get("TOTAL_RETRIES", 5)),
        initial_wait=float(os.environ.get("INITIAL_WAIT", 200)),
    )
    def _query_handler(self, query: str, language: str) -> dict:
        """Does the actual API call"""
        response_json: dict = {}
        parent = self.client.common_location_path(project=self.config.get("project_id"), location=self.config.get("location"))
        request = ekg.SearchRequest(
            parent=parent,
            query= query,
            languages=language,
            types= self.config.get("types"),
            limit= self.config.get("limit", 1))
        try:
            response = self.client.search(request=request)
            response_json = MessageToDict(response._pb, including_default_value_fields=True)
        except Exception as err:
            raise Exception(f"Unexpected error: {err}") from err

        return response_json

    def run_query(self):
        """Handles the query results"""
        date = datetime.strftime(datetime.now(), "%Y-%m-%d")
        results = []
        for query, languages in self.config["queries"].items():
            payload: dict = self._query_handler(query, languages)
            if payload:
                # add metadata of date, query and language
                query_partition: str = self.query_partition(query, languages)
                payload.update(
                    {
                        "date": date,
                        "query": query,
                        "language": languages,
                        "query_partition": query_partition,
                    }
                )
                results.append(payload)
                self.is_success()
                print(
                    f"Got data for query:'{query}' language:'{languages}' on '{date}'"
                )
            if not payload:
                self.not_success()
                print(
                    f"No data for query:'{query}' language:'{languages}' on '{date}'"
                )
        # only return if we have daa in the results list
        if results:
            return {"date": date, "data": results}
        self.dataset = results
        return
