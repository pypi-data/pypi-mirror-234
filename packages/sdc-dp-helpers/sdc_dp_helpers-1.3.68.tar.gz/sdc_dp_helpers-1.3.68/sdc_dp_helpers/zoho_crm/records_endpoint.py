"""MODULE FOR RECORDS ZOHO CRM DATA"""
# pylint: disable=arguments-differ,too-few-public-methods,inconsistent-return-statements,unused-argument,too-many-locals,broad-except,too-many-branches
import sys
import os
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any

from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
from zcrmsdk.src.com.zoho.crm.api.util.choice import Choice
from zcrmsdk.src.com.zoho.crm.api.users.user import User
from zcrmsdk.src.com.zoho.crm.api.layouts.layout import Layout
from zcrmsdk.src.com.zoho.crm.api.roles.role import Role
from zcrmsdk.src.com.zoho.crm.api.profiles.profile import Profile
from zcrmsdk.src.com.zoho.crm.api.record.record import Record

from zcrmsdk.src.com.zoho.crm.api.record import RecordOperations
from zcrmsdk.src.com.zoho.crm.api.record import (
    GetRecordsParam,
    GetRecordsHeader,
    APIException,
    ResponseWrapper,
)
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler
from sdc_dp_helpers.api_utilities.date_managers import date_string_handler


class InternalError(Exception):
    """
    Internal Server Error
    Resolution: Unexpected and unhandled exception in Server. Contact support team.
    """


class ErrorHandler:
    """class to handle errors"""

    def __init__(self):
        self.errors: list = []

    def append_error(self, module: str, error):
        """method to add errors to list"""
        self.errors.append({module: error})

    def get_errors(self):
        """method to return the error list"""
        return "\n".join([str(err) for err in self.errors])


class RequestHandler(ABC):
    """Base class to handle API calls"""

    @abstractmethod
    def api_call(self, **kwargs):
        """class method to make API calls"""
        raise NotImplementedError


class RecordsEndpointHandler:
    """Endpoint Handler for Records"""

    def __init__(self, configs: dict):
        self.configs = configs
        self.file_size_limit = self.configs.get("file_size_limit", 104857)
        self.error_handler = ErrorHandler()
        self.request_handler: RequestHandler = RecordsRequestHandler(
            error_handler=self.error_handler
        )

    def paginate(self, module_name: str, **kwargs):
        """Function to paginate through the whole dataset"""
        result_array: List[Dict[Any, Any]] = []
        current_size: int = 0
        more_records: bool = True
        page: int = self.configs.get("page", 1)
        page_limit: int = self.configs.get("page_limit")
        partition_counter: int = 0
        while more_records:
            print(f"fetching data for {module_name} page : {page}")
            response = self.request_handler.api_call(
                module_name=module_name, page=page, configs=self.configs
            )
            if response is None:
                yield {"data": [], "partition_counter": None, "module_partition": None}
                break

            request_info, results = response
            if request_info is not None:
                more_records: bool = request_info.get_more_records()

            for row in results["data"]:
                result_array.append(row)
                current_size += sys.getsizeof(row)
                if current_size >= self.file_size_limit:
                    yield {
                        "data": result_array,
                        "partition_counter": partition_counter,
                        "module_partition": results["module_partition"],
                    }
                    result_array = []
                    current_size: int = 0
                partition_counter += 1
            if result_array:
                yield {
                    "data": result_array,
                    "partition_counter": partition_counter,
                    "module_partition": results["module_partition"],
                }
            if page_limit is not None and page >= page_limit:
                print("early exit we have reached page limit")
                break

            page += 1


class RecordsRequestHandler(RequestHandler):
    """Requests Handler for Records Endpoint"""

    def __init__(self, error_handler):
        self.error_handler = error_handler

    @staticmethod
    def process_more_columns(column_name: str, value):
        """Method to process the data"""
        if isinstance(value, (User, Layout, Profile, Role)):
            return column_name, str(value.get_id())
        if isinstance(value, Choice):
            return column_name, value.get_value()
        if isinstance(value, Record):
            return column_name, value.get_id()
        return column_name, str(value)

    @staticmethod
    def build_query(configs: dict, cvid: Union[str, None], page: int, page_token=None):
        """build query to be run by the reader"""

        time_format = configs.get("time_format", "%Y-%m-%dT00:00:01+00:00")
        modified_since = date_string_handler(
            configs.get("modified_since", "50_years_ago"), time_format=time_format
        )
        param_instance = ParameterMap()
        param_instance.add(
            GetRecordsParam.converted, str(configs.get("converted", "both")).lower()
        )

        if page_token is None:
            param_instance.add(GetRecordsParam.page, page)
            param_instance.add(GetRecordsParam.per_page, configs["per_page"])
        if cvid is not None:
            print("adding cvid")
            param_instance.add(GetRecordsParam.cvid, str(cvid))
        if configs.get("sort_by") and cvid is None:
            param_instance.add(GetRecordsParam.sort_order, configs.get("sort_order"))
            param_instance.add(GetRecordsParam.sort_by, configs["sort_by"])
        param_instance.add(
            GetRecordsParam.include_child, str(configs["include_child"]).lower()
        )
        header_instance = HeaderMap()
        header_instance.add(
            GetRecordsHeader.if_modified_since,
            modified_since,  # configs["modified_since"]
        )
        print(modified_since)
        return param_instance, header_instance

    @retry_handler(
        exceptions=ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @retry_handler(
        exceptions=InternalError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 5)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def api_call(self, module_name: str, page: int, configs: dict, page_token=None):
        """calls the api call handler"""
        cvid = None
        request_info = None
        module_prefix = ""
        modulename_combination = module_name.rsplit("-", maxsplit=1)
        module_name = modulename_combination[0]
        if len(modulename_combination) > 1:
            module_prefix = modulename_combination[1]

        try:
            if configs.get("cvid") and module_prefix.startswith("CustomView"):
                cvid = configs["cvid"].get(f"{module_name}-{module_prefix}")

            param_instance, header_instance = self.build_query(
                configs=configs, cvid=cvid, page=page, page_token=page_token
            )

            response = RecordOperations().get_records(
                module_name, param_instance, header_instance
            )
            if (response is None) or (response.get_status_code() in [204, 304]):
                if response is not None:
                    print(
                        f"{module_name} returned No Content"
                        if response.get_status_code() == 204
                        else f"{module_name} returned Not Modified"
                    )
                return

            # Get object from response
            response_object = response.get_object()
            if response_object is None:
                return
            # Check if expected ResponseWrapper instance is received.
            if isinstance(response_object, ResponseWrapper):
                record_list = response_object.get_data()
                request_info = response_object.get_info()
                result_dict: Dict[Any, Any] = {}
                result_array: List[Dict[Any, Any]] = []
                for _, record in enumerate(record_list):
                    for key, value in record.get_key_values().items():
                        key, value = self.process_more_columns(key, value)
                        result_dict.update({key: value})
                    result_array.append(result_dict)
                    result_dict: Dict[Any, Any] = {}
                module_partition = f"{module_name}"
                if cvid is not None:
                    module_partition = f"{module_name}_{cvid}"
                return request_info, {
                    "module_partition": module_partition,
                    "data": result_array,
                }

            # Check if the request returned an exception
            if isinstance(response_object, APIException):
                error_code = response_object.get_code().get_value()
                error_details = response_object.get_details()
                self.error_handler.append_error(
                    module_name, f"{error_code}, {str(error_details)}"
                )
                if error_code == "INTERNAL_ERROR":
                    raise InternalError(
                        f"{module_name} {error_code}, {str(error_details)}"
                    )
            return

        except SDKException as exc:
            if "ConnectionError" in str(exc):
                raise ConnectionError(exc) from exc
            self.error_handler.append_error(module_name, exc.error_message)
        except Exception as exc:
            self.error_handler.append_error(module_name, exc.args[0])
        return
