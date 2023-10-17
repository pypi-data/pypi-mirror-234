"""MODULE FOR FETCHING ZOHO CRM DATA"""
# pylint: disable=arguments-differ,too-few-public-methods,duplicate-code,broad-except,unused-variable

from pathlib import Path
from typing import Dict, Any
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException

# from zcrmsdk.src.com.zoho.crm.api.request_proxy import RequestProxy
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer

from sdc_dp_helpers.zoho_crm.users_endpoint import UsersEndpointHandler
from sdc_dp_helpers.zoho_crm.records_endpoint import RecordsEndpointHandler
from sdc_dp_helpers.zoho_crm.bulk_endpoint import BulkEndpointHandler

from sdc_dp_helpers.api_utilities.retry_managers import retry_handler


class Authenticator:
    """Authenticator class"""

    def __init__(self, creds: dict):
        self.creds = creds
        self.current_path = Path(__file__).parent.resolve()

    @staticmethod
    def fetch_or_create_path(folder_path: str):
        """helper to ensure the path exists"""
        root_dir = Path(__file__).parent.resolve()
        if folder_path is not None or folder_path.strip() != ".":
            root_dir = f"{root_dir}/{folder_path}"

        Path(f"{root_dir}").mkdir(parents=True, exist_ok=True)
        return root_dir

    @retry_handler(
        exceptions=ConnectionError, total_tries=3, initial_wait=2, backoff_factor=2
    )
    def authenticate(self):
        """authenticator class method"""
        try:
            store = FileStore(
                file_path=f"{self.fetch_or_create_path('secrets/persistence')}/secrets.txt"
            )
            environment = USDataCenter.PRODUCTION()
            token = OAuthToken(
                client_id=self.creds["client_id"],
                client_secret=self.creds["client_secret"],
                token=self.creds["refresh_token"],
                token_type=TokenType.REFRESH,
                redirect_url=self.creds["redirect_uri"],
            )
            logger = Logger.get_instance(
                level=Logger.Levels.INFO,
                file_path=f"{self.fetch_or_create_path('logs')}/python_sdk_log.log",
            )
            # Create an UserSignature instance that takes user Email as parameter
            resource_path = self.fetch_or_create_path(".")
            user = UserSignature(email=self.creds["currentUserEmail"])
            config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

            Initializer.initialize(
                user=user,
                environment=environment,
                token=token,
                store=store,
                sdk_config=config,
                resource_path=resource_path,
                logger=logger,
                # proxy=request_proxy
            )
        except SDKException as exc:
            print("Error at authentication")
            if "ConnectionError" in str(exc):
                raise ConnectionError(exc) from exc

        return store


class HandledExceptionsError(Exception):
    """class for exceptions that we handled during the api run"""


class ZohoCRMAPI:
    """Sample"""

    def __init__(
        self,
        creds: Dict[Any, Any],
        configs: Dict[Any, Any],
    ):
        self.creds = creds
        self.configs = configs
        self.authenticator = Authenticator(creds=self.creds)
        self.service = self.authenticator.authenticate()
        self.file_size_limit = self.configs.get("file_size_limit", 104857)

    def get_end_point_handler(self, end_point: str):
        """Gets the API Handler to use in getting data"""
        endpoints = {
            "bulk": BulkEndpointHandler,
            "records": RecordsEndpointHandler,
            "users": UsersEndpointHandler,
        }
        if end_point not in endpoints:
            raise KeyError(f"provided endpoint not yet implemented: {end_point}")

        return endpoints[end_point](configs=self.configs)

    def fetch_data(self):
        """method to fetch data"""
        end_point: str = self.configs["end_point"]
        endpoint_handler = self.get_end_point_handler(end_point)
        modules = (
            self.configs["modules"] if end_point != "users" else self.configs["type"]
        )
        for module_name in modules:
            response = endpoint_handler.paginate(module_name=module_name)
            yield from response
        if endpoint_handler.error_handler.errors:
            raise HandledExceptionsError(endpoint_handler.error_handler.get_errors())
