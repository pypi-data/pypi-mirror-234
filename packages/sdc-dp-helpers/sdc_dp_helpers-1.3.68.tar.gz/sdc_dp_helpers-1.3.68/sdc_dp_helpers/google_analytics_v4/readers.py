"""
    CUSTOM READER CLASS
"""
# pylint: disable=too-few-public-methods,import-error,unused-import,redefined-outer-name
from typing import Dict, List, Any
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    RunReportRequest,
)


from sdc_dp_helpers.api_utilities.date_managers import date_range_iterator
from sdc_dp_helpers.api_utilities.file_managers import load_file


class GAV4Reader:
    """
    GOOGLE ANALYTICS V4 READERS CLASS
    """

    def __init__(self, configs_file_path: str, service_account_file_path: str):
        self.configs = load_file(configs_file_path, fmt="yml")
        self.service_account_file_path = service_account_file_path
        self._client = self._get_client()
        self.dataset = []
        self.api_calls = 0

    def _get_client(self):
        client = BetaAnalyticsDataClient().from_service_account_json(
            self.service_account_file_path
        )
        return client

    def _normalize(self, data, property_id: str) -> List[Dict[Any, Any]]:
        """Normalizes Data to Dictionary Format"""
        list_dataset = []
        dimension_headers = data.dimension_headers
        metric_headers = data.metric_headers

        for idx, row in enumerate(data.rows):
            row_data = {
                "property_id": property_id,
                "profile_name": self.configs["property_ids"][property_id],
            }

            for idx, dim_value_key in enumerate(row.dimension_values):
                row_data[dimension_headers[idx].name] = dim_value_key.value

            for idx, metric_value_key in enumerate(row.metric_values):
                row_data[metric_headers[idx].name] = metric_value_key.value

            list_dataset.append(row_data)
            # print(row_data)
        return list_dataset

    @staticmethod
    def build_multi_dimension_filter(config):
        for field_name, value in config.items():
            in_list_filter = Filter.InListFilter(values=value)
            dimension_filter = FilterExpression(
                filter=Filter(
                    field_name=field_name,
                    in_list_filter=in_list_filter,
                )
            )
        return dimension_filter

    def _query_handler(self, property_id: str, start_date: str, end_date: str):
        """Runs a simple report on a Google Analytics 4 property."""
        # Explicitly use service account credentials by specifying
        # the private key file.
        # query = self.build_query(property_id,date)
        # request = RunReportRequest(**query)
        if self.configs.get("filters") is None:
            request = RunReportRequest(
                property=f"properties/{property_id}",
                dimensions=[Dimension(name=dim) for dim in self.configs["dimensions"]],
                metrics=[Metric(name=metric) for metric in self.configs["metrics"]],
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                limit=self.configs.get("limit", 100000),
            )
        else:
            request = RunReportRequest(
                property=f"properties/{property_id}",
                dimensions=[Dimension(name=dim) for dim in self.configs["dimensions"]],
                metrics=[Metric(name=metric) for metric in self.configs["metrics"]],
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                dimension_filter=self.build_multi_dimension_filter(
                    self.configs.get("filters")
                ),
                limit=self.configs.get("limit", 100000),
            )
        self.api_calls += 1
        response = self._client.run_report(request)
        return response
        # [END analyticsdata_json_credentials_run_report]

    def run_query(self):
        """Controls the Flow of Query"""
        try:
            for property_id in self.configs["property_ids"]:
                for start_date, end_date in date_range_iterator(
                    start_date=self.configs["start_date"],
                    end_date=self.configs["end_date"],
                    interval=self.configs["interval"],
                    end_inclusive=True,
                    time_format="%Y-%m-%d",
                ):
                    payload = self._query_handler(
                        property_id=property_id,
                        start_date=start_date,
                        end_date=end_date,
                    )
                    if payload:
                        dataset: List[Dict] = self._normalize(payload, property_id)
                        yield {
                            "date": start_date,
                            "property_id": property_id,
                            "data": dataset,
                        }
                        self.dataset = dataset
        except Exception as error:
            print(f"Number of api calls made before this error {self.api_calls}")
            raise error
        finally:
            print(f"Current number of api calls: {self.api_calls}")
