"""CUSTOM MODULE TO WRITE GOOGLE SEARCH CONSOLE DATA"""
# pylint: disable=import-error, too-few-public-methods, unused-import, too-many-arguments, line-too-long
from datetime import datetime
from typing import Union, List, Any, Dict, Tuple, Optional
from sdc_dp_helpers.base_writers import BaseWriter


class GoogleSearchConsoleWriter(BaseWriter):
    """WRITER FOR Google Search Console RECRUIT DATA"""

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
                                                                          data to be written
        """
        # confirm the payload keys are matching accurately with what is expected
        if not {"data", "date", "dimension"}.issubset(set(payload.keys())):
            raise KeyError("invalid payload expecting: data, date, dimension")

        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")

        try:
            datetime.strptime(payload["date"], "%Y%m%d")
        except ValueError as exc:
            raise ValueError(
                f"wrong date value expected format YYYYMMDD: {payload['date']}"
            ) from exc

        if not isinstance(payload["dimension"], str):
            raise TypeError(f"wrong 'dimension' value passed: {payload['dimension']}")

        data: list = payload["data"]
        date: str = payload["date"]
        dimension: str = payload["dimension"]
        date_partition: str = f"date={date}"
        path_components = self.folder_path.split('/')
        path = f"{path_components[0]}/{date_partition}/{path_components[1]}/{path_components[2]}"

        write_path: str = f"{path}/{dimension}/{date}"
        return write_path, data
