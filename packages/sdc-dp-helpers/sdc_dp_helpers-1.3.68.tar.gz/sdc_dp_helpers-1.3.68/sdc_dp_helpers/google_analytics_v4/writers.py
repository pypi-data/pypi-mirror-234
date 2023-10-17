"""CUSTOM MODULE TO WRITE ZOHO RECRUIT DATA"""
# pylint: disable=too-few-public-methods, too-many-arguments
from typing import Union, List, Any, Dict, Tuple, Optional
from sdc_dp_helpers.base_writers import BaseWriter


class GAV4Writer(BaseWriter):
    """WRITER FOR GA V4 DATA"""

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
        # confirm the payload keys are matching accurately with what is expected
        if list(payload.keys()).sort() != ["data", "date", "property_id"].sort():
            raise KeyError("Invalid payload")
        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")
        if not isinstance(payload["property_id"], str):
            raise TypeError("invalid property_id passed: expected string")
        _property_id= payload.get("property_id")
        _date = payload.get("date")
        if _date:
            _date = _date.replace("-", "")
        else:
            raise KeyError("Date cannot be None")
        _data = payload.get("data")
        write_path: str = f"{self.folder_path}/{_property_id}/{_date}"

        return write_path, _data
