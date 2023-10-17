"""CUSTOM MODULE TO WRITE GOOGLE POSTMASER ANALYTICS DATA"""
# pylint: disable=too-few-public-methods, too-many-arguments
from typing import Union, List, Any, Dict, Tuple, Optional
from datetime import datetime
from sdc_dp_helpers.base_writers import BaseWriter


class GooglePostmasterWriter(BaseWriter):
    """WRITER FOR POSTMASTER DATA"""

    def __init__(
        self,
        bucket: str,
        folder_path: str,
        destination: str,
        configs: Optional[Dict[str, Any]] = None,
        clear_destination: bool = False,
    ):
        self.success: List[bool] = []
        super().__init__(
            bucket=bucket,
            folder_path=folder_path,
            destination=destination,
            configs=configs,
        )

    def verify_data(
        self, payload: Union[List[Dict[Any, Any]], Dict[Any, Any], Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[str, Any]): expecting a dictionary having data, date and dimension

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
                                                                          data to be written
        """
        # confirm the payload keys are matching accurately with what is expected
        if not {"date", "brand", "data"}.issubset(set(payload.keys())):
            raise KeyError("invalid payload expecting: date, brand and data.")

        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")

        try:
            datetime.strptime(payload["date"], "%Y%m%d")
        except ValueError as exc:
            raise ValueError(
                f"wrong date value expected format YYYYMMDD: {payload['date']}"
            ) from exc

        if not isinstance(payload["brand"], str):
            raise TypeError(f"wrong 'brand' value passed: {payload['brand']}")

        data: list = payload["data"]
        date: str = payload["date"]
        write_path: str = f"{self.folder_path}/{date}"
        return write_path, data
