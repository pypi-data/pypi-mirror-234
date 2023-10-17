"""CUSTOM MODULE TO WRITE ZOHO RECRUIT DATA"""
# pylint: disable=too-few-public-methods, too-many-arguments
from typing import Union, List, Any, Dict, Tuple, Optional
from datetime import datetime
from sdc_dp_helpers.base_writers import BaseWriter


class ZohoRecruitWriter(BaseWriter):
    """WRITER FOR ZOHO RECRUIT DATA"""

    def __init__(
        self,
        bucket: str,
        folder_path: str,
        destination: str,
        configs: Optional[Dict[str, Any]] = None,
        clear_destination: bool = False,
    ):
        self.success: List[bool] = []
        self.current_destination: Union[str, None] = None
        super().__init__(
            bucket=bucket,
            folder_path=folder_path,
            destination=destination,
            configs=configs,
            clear_destination=clear_destination,
        )

    def verify_data(
        self, payload: Dict[str, Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[str, Any]): expecting a dictionary having data, date and dimension

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
        """
        if not {"data", "module", "start_page"}.issubset(set(payload.keys())):
            raise KeyError("invalid payload expecting: data, module, stage_page")

        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")

        if not isinstance(payload["module"], str):
            raise TypeError("invalid data passed: expected string")

        if not isinstance(payload["start_page"], int):
            raise TypeError("invalid start_page value: expected integer")

        try:
            datetime.strptime(payload["date"], "%Y%m%d")
        except ValueError as exc:
            raise ValueError(
                f"wrong date value expected format YYYYMMDD: {payload['date']}"
            ) from exc

        data: list = payload["data"]
        module: str = payload["module"]
        start_page: int = payload["start_page"]
        date: str = payload["date"]

        write_path: str = f"{self.folder_path}/{module}/{date}_{start_page}"

        return write_path, data
