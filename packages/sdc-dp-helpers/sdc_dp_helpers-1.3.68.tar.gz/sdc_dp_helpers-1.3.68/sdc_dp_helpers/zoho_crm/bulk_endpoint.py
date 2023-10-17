"""MODULE TO GET DATA FROM BULK ENDPOINT"""
# pylint: disable=too-few-public-methods,arguments-differ,too-many-nested-blocks,inconsistent-return-statements,too-many-locals,too-many-branches
import os
import sys
from csv import DictReader
from io import TextIOWrapper
from zipfile import ZipFile
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any
from zcrmsdk.src.com.zoho.crm.api.bulk_read import (
    BulkReadOperations,
    RequestWrapper,
    FileBodyWrapper,
    APIException,
    Query,
    CallBack,
    Criteria,
    ActionWrapper,
    SuccessResponse,
    ResponseWrapper,
)
from zcrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException
from zcrmsdk.src.com.zoho.crm.api.util.choice import Choice
from zcrmsdk.src.com.zoho.crm.api.users.user import User
from zcrmsdk.src.com.zoho.crm.api.layouts.layout import Layout
from zcrmsdk.src.com.zoho.crm.api.record.record import Record
from zcrmsdk.src.com.zoho.crm.api.roles.role import Role
from zcrmsdk.src.com.zoho.crm.api.profiles.profile import Profile

from sdc_dp_helpers.api_utilities.date_managers import date_string_handler
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler


class ResourceNotFoundError(Exception):
    """
    The requested resource doesn't exist.
    Resolution: The job ID specified is invalid. Specify a valid job ID.
    """


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


class EndpointHandler:
    """class to create bulk job for export"""

    def make_api_call(self, **kwargs):
        """calls the request handler class"""
        raise NotImplementedError


class BulkEndpointHandler(EndpointHandler):
    """Endpoint handler for bulk api"""

    def __init__(self, configs: dict):
        self.configs = configs
        self.file_size_limit = configs.get("file_size_limit", 5242880)
        self.error_handler = ErrorHandler()
        self.create_bulk_read = CreateBulkReadRequestHandler(
            configs=configs, error_handler=self.error_handler
        )
        self.check_status = CheckBulkReadRequestHandler(
            error_handler=self.error_handler
        )
        self.download_result = DownloadResultRequestHandler(
            error_handler=self.error_handler
        )

    @staticmethod
    def process_more_columns(column_name: str, value):
        """Method to process the data"""
        if isinstance(value, (User, Layout, Profile, Role)):
            return column_name, {
                "id": value.get_id(),
                "name": value.get_name(),
            }
        if isinstance(value, Choice):
            return column_name, value.get_value()
        if isinstance(value, Record):
            return column_name, value.get_id()
        return column_name, str(value)

    def make_api_call(self, module_name: str, job_id: int, destination_folder: str):
        """make api call to fetch data"""
        yield from self.download_result.api_call(
            module_name=module_name,
            job_id=job_id,
            destination_folder=destination_folder,
        )

    def paginate(self, module_name: str):
        """paginate through the pages"""
        result_array: List[Dict[Any, Any]] = []
        current_size: int = 0
        more_records: bool = True
        page: int = self.configs.get("page", 1)
        page_limit: int = self.configs.get("page_limit")
        destination_folder: str = self.configs.get("destination_folder", "data_folder")
        while more_records:
            more_records = False
            job_creation = self.create_bulk_read.api_call(
                module_name=module_name, configs=self.configs, page=page
            )
            if (
                not isinstance(job_creation, dict)
                or job_creation.get("results", {"id": None}).get("id") is None
            ):
                break
            job, module_partition = (
                job_creation["results"],
                job_creation["module_partition"],
            )
            print(job)

            job_status: dict = self.check_status.api_call(
                module_name=module_name, job_id=job["id"]
            )
            if isinstance(job_status, dict) and job_status.get("download_url"):
                print(job_status)
                results = self.make_api_call(
                    module_name=module_name,
                    job_id=job["id"],
                    destination_folder=destination_folder,
                )
                counter = 0
                for result in results:
                    result_array.append(result)
                    current_size += sys.getsizeof(result)
                    if current_size >= self.file_size_limit:
                        yield {
                            "module_partition": module_partition,
                            "partition_counter": counter,
                            "data": result_array,
                        }
                        result_array: List[Dict[Any, Any]] = []
                        current_size = 0
                    counter += 1

                if result_array:
                    yield {
                        "module_partition": module_partition,
                        "partition_counter": counter,
                        "data": result_array,
                    }
                more_records = job_status.get("more_records", False)
                if more_records is False:
                    break

                if page_limit is not None and page >= page_limit:
                    print("early exit we have reached page limit")
                    break

                page += 1


class CreateBulkReadRequestHandler:
    """Handler to Create Bulk Job"""

    def __init__(self, configs: dict, error_handler):
        self.configs = configs
        self.error_handler = error_handler

    @staticmethod
    def process_more_columns(column_name: str, value):
        """Method to process the data"""
        if isinstance(value, (User, Layout, Profile, Role)):
            return column_name, {
                "id": value.get_id(),
                "name": value.get_name(),
            }
        if isinstance(value, Choice):
            return column_name, value.get_value()
        if isinstance(value, Record):
            return column_name, value.get_id()
        return column_name, str(value)

    def build_query(
        self, module_name: str, page: int, cvid: Union[str, None], configs: dict
    ):
        """method to build the query to be used for the api call"""
        # Get instance of CallBack Class
        call_back = CallBack()
        call_back.set_url("https://www.example.com/callback")  # Set valid callback URL
        call_back.set_method(Choice("post"))
        request = RequestWrapper()
        # The Bulk Read Job's details is posted to this URL
        # on successful completion / failure of the job.
        request.set_callback(call_back)
        query = Query()  # Get instance of Query Class
        query.set_module(module_name)

        # Specifies the unique ID of the custom view, whose records you want to export.
        if cvid is not None:
            query.set_cvid(str(cvid))

        # Specifies the API Name of the fields to be fetched
        if configs.get("select_fields"):
            query.set_fields(configs.get("select_fields"))
        # To set page value, By default value is 1.
        query.set_page(page)

        # Get instance of Criteria Class
        criteria = Criteria()
        criteria_group = configs["group"]
        criteria_datetime_fields = configs["criteria_datetime_fields"]
        for group in criteria_group:
            value = group["value"]
            api_name = group["api_name"]
            if api_name in criteria_datetime_fields:
                time_format = criteria_datetime_fields[api_name]
                value = [
                    date_string_handler(value[0], time_format=time_format).strftime(
                        time_format
                    ),
                    date_string_handler(value[1], time_format=time_format).strftime(
                        time_format
                    ),
                ]
                print(value)
            criteria.set_api_name(api_name)
            criteria.set_comparator(Choice(group["comparator"]))
            criteria.set_value(value)

        query.set_criteria(criteria)
        request.set_query(query)
        request.set_file_type(Choice("csv"))

        return request

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
    def api_call(self, module_name: str, configs: dict, page=1):
        """
        This method is used to create a bulk read job to export records.
        :param module_api_name: The API Name of the record's module
        module_name = 'Leads'
        """
        try:
            cvid = None
            module_prefix = ""
            modulename_combination = module_name.rsplit("-", maxsplit=1)
            module_name = modulename_combination[0]
            if len(modulename_combination) > 1:
                module_prefix = modulename_combination[1]
            if configs.get("cvid") and module_prefix.startswith("CustomView"):
                cvid = configs["cvid"].get(f"{module_name}-{module_prefix}")

            request = self.build_query(
                module_name=module_name, page=page, cvid=cvid, configs=configs
            )
            bulk_read_operations = BulkReadOperations()
            response = bulk_read_operations.create_bulk_read_job(request)

            if response is not None:
                response_object = response.get_object()

                if response_object is not None:
                    # Check if expected ActionWrapper instance is received.
                    if isinstance(response_object, ActionWrapper):
                        action_response_list = response_object.get_data()

                        for action_response in action_response_list:
                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                details = action_response.get_details()
                                result = {
                                    "status": action_response.get_status().get_value(),
                                    "code": action_response.get_code().get_value(),
                                    "id": int(details["id"]),
                                    "details": dict(
                                        [
                                            self.process_more_columns(key, value)
                                            for key, value in details.items()
                                        ]
                                    ),
                                    "message": action_response.get_message().get_value(),
                                }
                                module_partition = f"{module_name}"
                                if cvid is not None:
                                    module_partition = f"{module_name}_{cvid}"
                                return {
                                    "results": result,
                                    "module_partition": module_partition,
                                }

                            if isinstance(action_response, APIException):
                                error_code = action_response.get_code().get_value()
                                error_details = action_response.get_details()
                                # error_status = action_response.get_status().get_value()
                                self.error_handler.append_error(
                                    module_name, f"{error_code}, {str(error_details)}"
                                )

                    elif isinstance(response_object, APIException):
                        error_code = response_object.get_code().get_value()
                        error_details = response_object.get_details()
                        self.error_handler.append_error(
                            module_name, f"{error_code}, {str(error_details)}"
                        )
                        if error_code == "INTERNAL_ERROR":
                            raise InternalError(
                                f"{module_name} {error_code}, {str(error_details)}"
                            )
        except SDKException as exc:
            if "ConnectionError" in str(exc):
                raise ConnectionError(exc) from exc


class CheckBulkReadRequestHandler:
    """Check Bulk Read Job"""

    def __init__(self, error_handler):
        self.error_handler = error_handler

    @retry_handler(
        exceptions=ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @retry_handler(
        exceptions=InternalError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @retry_handler(
        exceptions=ResourceNotFoundError,
        total_tries=10,
        initial_wait=2,
        backoff_factor=2,
    )
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 5)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def api_call(self, module_name: str, job_id: int):
        """
        This method is used to get the details of a bulk read job performed previously.
        :param job_id: The unique ID of the bulk read job.
        job_id = 3409643000002461001
        """
        try:
            results = None
            bulk_read_operations = BulkReadOperations()
            response = bulk_read_operations.get_bulk_read_job_details(job_id)

            if response is not None:
                if response.get_status_code() in [204, 304]:
                    print(
                        "No Content"
                        if response.get_status_code() == 204
                        else "Not Modified"
                    )
                    return results

                response_object = response.get_object()

                if response_object is not None:
                    # Check if expected ResponseWrapper instance is received
                    if isinstance(response_object, ResponseWrapper):
                        # Get the list of JobDetail instances
                        job_details_list = response_object.get_data()

                        for job_detail in job_details_list:
                            # Get the Job ID of each jobDetail
                            criteria = job_detail.get_query().get_criteria()
                            results = {
                                "id": job_detail.get_id(),
                                "read_operation": job_detail.get_operation(),
                                "read_state": job_detail.get_state().get_value(),
                                "query": {
                                    "criteria": {
                                        "value": criteria.get_value(),
                                        "api_name": criteria.get_api_name(),
                                    },
                                    "cvid": job_detail.get_query().get_cvid(),
                                },
                            }

                            result = job_detail.get_result()

                            if result is not None:
                                results.update(
                                    {
                                        "page": str(result.get_page()),
                                        "count": str(result.get_count()),
                                        "download_url": result.get_download_url(),
                                        "per_page": str(result.get_per_page()),
                                        "more_records": result.get_more_records(),
                                    }
                                )

                            if (
                                isinstance(results["id"], int)
                                and results["read_state"] != "COMPLETED"
                            ):
                                raise ResourceNotFoundError(f"{module_name}, {results}")
                        return results

                    if isinstance(response_object, APIException):
                        error_code = response_object.get_code().get_value()
                        error_details = response_object.get_details()
                        self.error_handler.append_error(
                            module_name, f"{job_id} {error_code}, {str(error_details)}"
                        )
                        if error_code == "RESOURCE_NOT_FOUND":
                            raise ResourceNotFoundError(
                                f"{module_name} {error_code}, {str(error_details)}"
                            )
                        if error_code == "INTERNAL_ERROR":
                            raise InternalError(
                                f"{module_name} {error_code}, {str(error_details)}"
                            )

        except SDKException as exc:
            if "ConnectionError" in str(exc):
                raise ConnectionError(exc) from exc


class DownloadResultRequestHandler:
    """Download result handler for bulk api"""

    def __init__(self, error_handler):
        self.error_handler = error_handler

    @retry_handler(
        exceptions=ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @retry_handler(
        exceptions=InternalError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    @retry_handler(
        exceptions=ResourceNotFoundError,
        total_tries=10,
        initial_wait=2,
        backoff_factor=2,
    )
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 5)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def api_call(self, module_name: str, job_id: int, destination_folder: str):
        """
        This method is used to download the result of Bulk Read operation
        :param job_id: The unique ID of the bulk read job.
        :param destination_folder: The absolute path where downloaded file has to be stored.
        job_id = 3409643000002461001
        """
        try:
            # Get instance of BulkReadOperations Class
            bulk_read_operations = BulkReadOperations()
            response = bulk_read_operations.download_result(job_id)

            if response is not None:
                if response.get_status_code() in [204, 304]:
                    print(
                        "No Content"
                        if response.get_status_code() == 204
                        else "Not Modified"
                    )
                    return

                # Get object from response
                response_object = response.get_object()

                if response_object is not None:
                    # Check if expected FileBodyWrapper instance is received.
                    if isinstance(response_object, FileBodyWrapper):
                        stream_wrapper = response_object.get_file()
                        # Construct the file name by joining the destinationFolder
                        # and the name from StreamWrapper instance
                        Path(f"{destination_folder}").mkdir(parents=True, exist_ok=True)
                        file_name = os.path.join(
                            destination_folder, stream_wrapper.get_name()
                        )

                        with open(file_name, "wb") as dest:
                            # Get the stream from StreamWrapper instance
                            for chunk in stream_wrapper.get_stream():
                                dest.write(chunk)
                            dest.close()

                        with ZipFile(file_name) as zipfile:
                            for file in zipfile.filelist:
                                with zipfile.open(file) as file_contents:
                                    dict_reader = DictReader(
                                        TextIOWrapper(file_contents, encoding="utf-8")
                                    )
                                    yield from dict_reader

                    elif isinstance(response_object, APIException):
                        error_code = response_object.get_code().get_value()
                        error_details = response_object.get_details()
                        self.error_handler.append_error(
                            module_name, f"{job_id} {error_code}, {str(error_details)}"
                        )
                        if error_code == "RESOURCE_NOT_FOUND":
                            raise ResourceNotFoundError(
                                f"{module_name} {error_code}, {str(error_details)}"
                            )
                        if error_code == "INTERNAL_ERROR":
                            raise InternalError(
                                f"{module_name} {error_code}, {str(error_details)}"
                            )
        except SDKException as exc:
            if "ConnectionError" in str(exc):
                raise ConnectionError(exc) from exc
