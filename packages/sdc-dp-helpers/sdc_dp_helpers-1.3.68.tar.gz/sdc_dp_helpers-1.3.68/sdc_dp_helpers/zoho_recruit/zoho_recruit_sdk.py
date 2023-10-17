"""CUSTOM INTERFACES FOR ZOHO RECRUIT ENDPOINTS"""

# pylint: disable=broad-except,too-few-public-methods,too-many-arguments,arguments-differ, too-many-locals,abstract-method,unnecessary-dict-index-lookup,import-error
import sys
import os

from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from typing import Union, Any, List, Dict, Generator, Tuple

from io import BytesIO
from io import TextIOWrapper
from csv import DictReader
from zipfile import ZipFile

import requests

from requests.exceptions import HTTPError
from sdc_dp_helpers.api_utilities.date_managers import date_string_handler
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler, request_handler


class AuthenticationError(Exception):
    """Raised when our access token is invalid message INVALID_TOKEN"""


class APILimitError(Exception):
    """Error raised for exceeding API limits"""


class Authenticator:
    """Authenticator Class for Zoho Recruit"""

    def __init__(self):
        self.next_refresh: datetime = datetime.now()
        self.access_token: str = ""

    def get_access_token(
        self, sessions: requests.Session, secrets: Dict[Any, Any]
    ) -> str:
        """Authentication method

        Args:
            sessions (requests.Session): requests.Sessions
            secrets (Dict[Any, Any]): dictionary having secrets

        Returns:
            str : the access_token for zoho
        """
        response = {
            "access_token": None,
            "api_domain": "https://www.zohoapis.com",
            "token_type": "Bearer",
            "expires_in": 0,
        }
        try:
            response = sessions.post(
                url="https://accounts.zoho.com/oauth/v2/token?",
                params={
                    "refresh_token": secrets["refresh_token"],
                    "client_id": secrets["client_id"],
                    "client_secret": secrets["client_secret"],
                    "grant_type": "refresh_token",
                },
                timeout=61,
            ).json()
        except Exception as exc:
            print(f"Error on refreshing oauth_token {exc}")
        seconds_to_expiry = int(response["expires_in"]) - 100
        self.next_refresh = datetime.now() + timedelta(seconds=seconds_to_expiry)

        print(f"new oauth_token {response['access_token']}")
        print(f"next oauth_token_refresh {self.next_refresh}")
        self.access_token = response["access_token"]
        return response["access_token"]

    def get_refresh_token(
        self, sessions: requests.Session, secrets: Dict[str, str]
    ) -> Dict[str, Any]:
        """Gets refresh token and access toekn used by the api calls see url:
        https://www.zoho.com/recruit/developer-guide/apiv2/access-refresh.html

        Args:
            configs (Dict[str, str]): client_id, client_secret, code, grant_type, redirect_uri

        Returns:
            Dict[str, Any]: response with refresh_token and access_token
        """
        results = {
            "access_token": None,
            "refresh_token": None,
            "api_domain": "https://www.zohoapis.com",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        response = sessions.post(
            url=secrets.get("url", "https://accounts.zoho.com/oauth/v2/token"),
            params={
                "grant_type": "authorization_code",
                "client_id": secrets["client_id"],
                "client_secret": secrets["cleint_secrets"],
                "code": secrets["code"],
                "redirect_uri": "https://accounts.zoho.com/developerconsole",
            },
            timeout=60,
        )
        status_code = response.status_code
        if status_code != 200:
            print(
                f"error getting data from: {response.url} \nerror_details: {response.json()}\n"
            )
        if status_code == 200:
            results = response.json()
        return results

    def authenticate(self, **kwargs):
        """Authenticate Zoho Access"""
        if self.next_refresh <= datetime.now():
            self.get_access_token(**kwargs)
        return self.access_token


class RequestHandler(ABC):
    """Interface for API Call Method"""

    API_LIMIT_EXCEEDED_MESSAGE = "Exceeded API limits going to sleep"

    def __init__(self, session: requests.Session):
        self.session = session

    @abstractmethod
    def make_api_call(self, **kwargs):
        """Make API Call"""
        raise NotImplementedError


class CreateBulkJob(RequestHandler):
    """Creates Bulk Job"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(
        self, access_token: str, module: str, page: int, criteria: dict
    ) -> Tuple[Union[str, None], Union[str, None], Dict[Any, Any]]:
        """Create Bulk Job"""
        status, job_id, details = None, None, {"id": None}
        query = {"module": module, "page": page}
        query.update(criteria)
        print(query)
        response = self.session.post(
            url="https://recruit.zoho.com/recruit/bulk/v2/read",
            json={
                "query": query,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Zoho-oauthtoken {access_token}",
                # "If-Modified-Since": modified_since,
            },
            timeout=61,
        )
        status_code = response.status_code
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code not in [200, 201]:
            print(
                f"error getting data from: {response.url} \nerror_details: {response.json()}\n"
            )

        print(
            f"{query['module']} job creation attempt done with status_code: {status_code}"
        )
        if response.status_code in [200, 201]:
            json_data = response.json().get("data", [])[0]
            status = json_data["status"]
            job_id, details = json_data["details"]["id"], json_data["details"]

        return status, job_id, details


class CheckBulkJobStatus(RequestHandler):
    """Request Call to Check Bulk Job Status"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(
        self, access_token: str, job_id: str
    ) -> Tuple[Union[str, None], bool, Dict[Any, Any]]:
        """Check status of bulk job"""

        results = {"data": [{"id": job_id, "state": None, "result": {}}]}
        state, more_records = None, False
        response = self.session.get(
            url=f"https://recruit.zoho.com/recruit/bulk/v2/read/{job_id}",
            headers={
                "Authorization": f"Zoho-oauthtoken {access_token}",
            },
            timeout=61,
        )
        status_code = response.status_code
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code != 200:
            print(
                f"error getting data from: {response.url} \nerror_details: {response.json()}\n"
            )

        if status_code == 200:
            json_data = response.json()["data"][0]
            results = json_data.get("result", {"more_records": False})
            state, more_records = json_data["state"], results["more_records"]
            # page, record_count = results["page"], results["count"]
        return state, more_records, results


class BulkRequestHandler(RequestHandler):
    """Bulk Result Reader"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(self, access_token: str, job_id: str):
        """Download Bilk Data"""
        results = None
        response = self.session.get(
            url=f"https://recruit.zoho.com/recruit/bulk/v2/read/{job_id}/result",
            headers={
                "Authorization": f"Zoho-oauthtoken {access_token}",
            },
            timeout=61,
        )
        status_code, results = response.status_code, None
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code not in [200, 201]:
            print(
                f"error getting data from: {response.url}"
                f"status_code: {status_code}\nerror_details: {response.json()}\n"
            )

        if status_code:
            results = response.content
        return results


class AssessmentRequestHandler(RequestHandler):
    """Class for Making API Call"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(
        self,
        access_token: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            json={
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Zoho-oauthtoken {access_token}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )

        status_code, reason = response.status_code, response.reason
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code != 200:
            print(
                f"error getting data from: {response.url}"
                f"status_code: {status_code}\nerror_details: {response.json()}\n"
            )

        data, more_records = None, False
        if response.status_code == 200:
            results = response.json()
            data = results["Assessments"]
            more_records = False
        return data, more_records, status_code, reason


class RecordsRequestHandler(RequestHandler):
    """Class for Making API Call"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(
        self,
        access_token: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            params={
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Authorization": f"Zoho-oauthtoken {access_token}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )

        status_code, reason = response.status_code, response.reason
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code != 200:
            print(
                f"error getting data from: {response.url}"
                f"status_code: {status_code}\nerror_details: {response.json()}\n"
            )

        data, more_records = None, False
        if response.status_code == 200:
            results = response.json()
            data = results["data"]
            more_records = results.get("info", {"more_records": False}).get(
                "more_records"
            )
        return data, more_records, status_code, reason


class UsersRequestHandler(RequestHandler):
    """Class for Making API Call"""

    @retry_handler(exceptions=APILimitError, total_tries=5, initial_wait=180)
    @request_handler(
        wait=int(os.environ.get("API_WAIT_TIME", 30)),
        backoff_factor=0.01,
        backoff_method="random",
    )
    def make_api_call(
        self,
        access_token: str,
        url: str,
        page: int,
        per_page: int,
        sort_by: str,
        sort_order: str,
        modified_since: Union[str, None],
        **kwargs,
    ):
        response = self.session.get(
            url=url,
            json={
                "type": kwargs.get("users_type"),
                "page": page,
                "per_page": per_page,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Zoho-oauthtoken {access_token}",
                "If-Modified-Since": modified_since,
            },
            timeout=61,
        )

        status_code, reason = response.status_code, response.reason
        if status_code == 429:
            raise APILimitError(self.API_LIMIT_EXCEEDED_MESSAGE)

        if status_code != 200:
            print(
                f"error getting data from: {response.url}"
                f"status_code: {status_code}\nerror_details: {response.json()}\n"
            )

        data, more_records = None, False
        if response.status_code == 200:
            results = response.json()
            data = results["users"]
            more_records = results.get("info", {"more_records": False}).get(
                "more_records"
            )
        return data, more_records, status_code, reason


class APIRequestHandlerFactory:
    """Gets Us the API Call Handler"""

    def get_api_call_handler(self, method: str, session: requests.Session):
        """Gets for use the API Call Handler to Use"""
        api_call_handlers = {
            "assessments": AssessmentRequestHandler,
            "records": RecordsRequestHandler,
            "users": UsersRequestHandler,
            "bulk": BulkRequestHandler,
        }
        return api_call_handlers[method](session=session)


class ZohoRecruitAPI:
    """Sample"""

    authenticator = Authenticator()

    def __init__(
        self,
        session: requests.Session,
        secrets: Dict[Any, Any],
        file_size_limit: int = 104857,  # 5MB
    ):
        self.session = session
        self.secrets = secrets
        self.access_token = self.get_access_token()
        self.file_size_limit = file_size_limit

    def get_access_token(self):
        """Get zoho recruit oauth_token"""
        self.access_token = self.authenticator.authenticate(
            sessions=self.session, secrets=self.secrets
        )
        return self.access_token

    def get_end_point_handler(self, end_point: str):
        """Gets the API Handler to use in getting data"""
        endpoints = {
            "bulk": BulkEndpointHandler,
            "records": RecordsEndpointHandler,
            "users": UsersEndpointHandler,
        }
        if end_point not in endpoints:
            raise KeyError(f"provided endpoint not yet implemented: {end_point}")

        return endpoints[end_point](session=self.session, secrets=self.secrets)


class RestAPICaller(ZohoRecruitAPI):
    """Class to Call the RestAPI Endpoints"""

    def api_call(self, api_call_handler: RequestHandler, **kwargs):
        """Makes API Call"""
        results = None
        status_code = None
        reason = None
        more_records = True

        try:
            response = api_call_handler.make_api_call(
                access_token=self.access_token,
                url=kwargs.get("url"),
                module=kwargs.get("module"),
                page=kwargs.get("page"),
                per_page=kwargs.get("per_page"),
                sort_by=kwargs.get("sort_by"),
                sort_order=kwargs.get("sort_order"),
                modified_since=kwargs.get("modified_since"),
                users_type=kwargs.get("users_type"),
            )
            status_code, reason = response[2], response[3]
            results = response[0]
            more_records = response[1]

        except HTTPError as exc:
            print(
                f"error code: {exc.response.status_code} error message: {exc.response}"
            )
            if exc.response.status_code != 204:
                raise exc
        except requests.exceptions.JSONDecodeError:
            pass
        except Exception as err:
            print(f"failed with status {status_code} reason {reason}\n")
            raise err
        return results, more_records

    def paginate(
        self,
        api_call_handler: RequestHandler,
        module: str,
        configs: Dict[str, Any],
        **kwargs,
    ):  # List[Dict[Any, Any]]:
        """Method to actually make the API call

        Args:
            configs: dict of parameters and headers for the API call

        Returns:
            List[Dict[Any, Any]]: A list of dictionary of each response
        """

        result_array = []
        avg_record_size: int = 0
        current_size: int = 0
        page: int = configs.get("page", 1)
        per_page: int = configs.get("per_page", 200)
        modified_since: Union[None, str] = configs.get("modified_since")
        sort_by = configs.get("sort_by", "Modified_Time")
        sort_order = configs.get("sort_order", "desc")
        users_type = kwargs.get("users_type")
        page_limit: int = configs.get("page_limit", 1000)
        self.file_size_limit = configs.get("file_size_limit", 5242880)
        counter: int = 0
        base_url = "https://recruit.zoho.com/recruit/v2"

        more_records = True
        url = f"{base_url}/{module}"
        while more_records:
            print(
                f"getting module {module} page {page} "
                f"more_records {more_records} current_size {current_size}"
            )

            self.access_token = self.get_access_token()

            response = self.api_call(
                api_call_handler,
                url=url,
                module=module,
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
                modified_since=modified_since,
                users_type=users_type,
            )

            results, more_records = response[0], response[1]
            if results is None:
                yield {"start_page": page, "data": result_array}
                break

            if avg_record_size == 0:
                avg_record_size = sys.getsizeof(results[0])

            result_array = result_array + results
            current_size += avg_record_size
            if counter > page_limit:  # exit if we go past page_limit
                print(f"\nExiting, we have reached page_limit {page_limit}\n")
                yield {"start_page": page, "data": result_array}
                break
            counter += 1

            if (current_size >= self.file_size_limit) or (more_records is False):
                yield {"start_page": page, "data": result_array}
                result_array = []
                current_size = 0
            page += 1


class RecordsEndpointHandler(RestAPICaller):
    """Class to Handle Get Records Endpoint"""

    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Fetches the dat for records endpoint"""

        api_factory = APIRequestHandlerFactory()
        for module in configs["modules"]:
            method = "records" if module != "Assessments" else "assessments"

            api_call_handler = api_factory.get_api_call_handler(
                method, session=self.session
            )
            results = self.paginate(api_call_handler, module=module, configs=configs)
            for result in results:
                result["module"] = module
                yield result


class UsersEndpointHandler(RestAPICaller):
    """Handler Class for Users Endpoint"""

    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Fetches the dat for records endpoint"""

        api_factory = APIRequestHandlerFactory()
        method = "users"
        api_call_handler = api_factory.get_api_call_handler(
            method, session=self.session
        )
        users_types = configs.get("types", ["AllUsers"])
        for users_type in users_types:
            results = self.paginate(
                api_call_handler, module=method, configs=configs, users_type=users_type
            )
            for result in results:
                result["module"] = users_type
                yield result


class BulkAPICaller(ZohoRecruitAPI):
    """Calls the Bulk API"""

    def __init__(
        self,
        secrets: Dict[Any, Any],
        session: requests.Session,
        file_size_limit: int = 5242880,  # 5MB
    ):
        self.jobs: Dict[str, Any] = {}
        self.configs: Dict[Any, Any] = {}
        super().__init__(session, secrets, file_size_limit)
        self.check_status = CheckBulkJobStatus(self.session)
        self.create_job = CreateBulkJob(self.session)

    @staticmethod
    def criteria_datetime_processor(datetime_fields: dict, groups: list) -> list:
        """processor for datetime in criteria"""
        final_groups = []
        for group in groups:
            api_name = group["api_name"]
            if api_name in datetime_fields:
                start = datetime.strftime(
                    date_string_handler(group["value"][0]),
                    datetime_fields.get(api_name, "%Y-%m-%dT00:00:00+00:00"),
                )
                end = datetime.strftime(
                    date_string_handler(group["value"][1]),
                    datetime_fields.get(api_name, "%Y-%m-%dT00:00:00+00:00"),
                )
                group["value"] = [start, end]

            final_groups.append(group)

        start_end = [
            key["value"] for key in final_groups if key["api_name"] == "Modified_Time"
        ]
        if start_end == []:
            raise KeyError("provide `Modified_Time` as a default filter in `group`")
        group = [
            {
                "api_name": "Modified_Time",
                "value": [start_end[0][0], start_end[0][1]],
                "comparator": "between",
            },
        ]

        return final_groups

    @staticmethod
    def build_bulk_query(
        local_configs: dict, criteria_group: list, module: str
    ) -> dict:
        """Method used to build the query to send
        https://www.zoho.com/recruit/developer-guide/apiv2/bulk-read/create-job.html
        """

        group = []
        if module in ["Candidates"]:
            for item in criteria_group:
                if item["api_name"] == "Modified_Time":
                    new_item = {}
                    new_item["api_name"] = "Last_Activity_Time"
                    new_item.update(
                        {key: value for key, value in item.items() if key != "api_name"}
                    )
                    group.append(new_item)
                    continue
                if item["api_name"] == "Created_Time":
                    group.extend([item, item])
                    continue
                group.append(item)
            criteria_group = group

        query = {
            "selectfields": local_configs.get("select_fields", []),
            "criteria": {
                "group_operator": local_configs.get("group_comparator", "and"),
            },
        }
        query["criteria"]["group"] = criteria_group
        if local_configs.get("cvid") is not None:
            query["cvid"] = local_configs.get("cvid")

        return query

    def wait_for_download(self, job_id: str) -> Tuple[bool, int]:
        """Method to keep checking for download status"""

        state: str = ""
        proceed: bool = False
        page: int = 1
        record_count: int = 0
        more_records: bool = False
        total_wait_time, wait_threshold = 0, 600
        while (state != "COMPLETED") or (total_wait_time > wait_threshold):
            self.access_token: str = self.get_access_token()
            state, more_records, results = self.check_status.make_api_call(
                access_token=self.access_token, job_id=job_id
            )
            page, record_count = results.get("page"), results.get("count")

            if state == "COMPLETED":
                proceed = True
                break

        print(
            f"page: {page}, record_count: {record_count}, more_records: {more_records}"
        )
        return proceed, record_count

    @staticmethod
    def parse_zip_file(response):
        """Parse the zip file"""
        # data_array: List[Dict[Any, Any]] = []
        with ZipFile(BytesIO(response)) as zipfile:
            for file in zipfile.filelist:
                with zipfile.open(file) as file_contents:
                    dict_reader = DictReader(
                        TextIOWrapper(file_contents, encoding="utf-8")
                    )
                    yield from dict_reader

    def api_call(self, api_call_handler: RequestHandler, **kwargs):
        """Makes api call"""
        job_id: str = kwargs["job_id"]
        download_status = self.wait_for_download(job_id=job_id)
        if download_status[0] is True and download_status[1] > 0:
            self.access_token = self.get_access_token()
            response = api_call_handler.make_api_call(
                access_token=self.access_token, job_id=job_id
            )
            yield from self.parse_zip_file(response)

    def paginate(self, api_call_handler: RequestHandler, module, configs, criteria):
        """Paginator Function Through the Pages"""

        result_array = []
        current_size: int = 0
        more_records = True
        self.file_size_limit = configs.get("file_size_limit", 5242880)

        page = 1

        while more_records:
            status, job_id, _ = self.create_job.make_api_call(
                self.access_token, module, page, criteria
            )

            print(f"bulk_job status: {status} and job_id : {job_id}")
            state, more_records, _ = self.check_status.make_api_call(
                self.access_token, job_id
            )
            if job_id is not None:
                self.jobs[job_id] = {"state": state, "downloaded": False}

            page += 1

        for job_id, values in self.jobs.items():
            if values["downloaded"] is True:
                continue
            results = self.api_call(api_call_handler, job_id=job_id)
            if not results:
                print(f"No data for job_id {job_id}")
                continue
            counter = 0
            for result in results:
                self.jobs[job_id]["downloaded"] = True
                result_array.append(result)
                current_size += sys.getsizeof(result)
                if current_size >= self.file_size_limit:
                    yield {"start_page": counter, "data": result_array}
                    result_array = []
                    current_size = 0
                counter += 1

            if result_array:
                yield {"start_page": counter, "data": result_array}


class BulkEndpointHandler(BulkAPICaller):
    """Handler for Mkaing the Download Call"""

    def fetch_data(
        self, configs: dict
    ) -> Generator[Dict[str, Union[str, List[Dict[Any, Any]]]], None, None]:
        """Code to fetch the data"""

        method = "bulk"
        criteria = {}
        criteria_group = self.criteria_datetime_processor(
            configs.get("criteria_datetime_fields", {}), configs["group"]
        )
        for module in configs["modules"]:
            criteria = self.build_bulk_query(
                local_configs=configs,
                criteria_group=criteria_group,
                module=module,
            )

            api_factory = APIRequestHandlerFactory()
            api_call_handler = api_factory.get_api_call_handler(
                method, session=self.session
            )
            results = self.paginate(
                api_call_handler, module=module, configs=configs, criteria=criteria
            )
            for result in results:
                result["module"] = module
                yield result
