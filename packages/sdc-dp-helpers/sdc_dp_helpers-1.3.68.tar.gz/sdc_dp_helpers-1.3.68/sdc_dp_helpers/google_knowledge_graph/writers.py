# pylint: disable=import-error, too-few-public-methods, unused-import, too-many-arguments, line-too-long
"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import re
from typing import Union, List, Any, Dict, Tuple, Optional
from sdc_dp_helpers.base_writers import BaseWriter


class GoogleKnowledgeGraphWriter(BaseWriter):
    """GoogleKnowledgeGraphReader Class"""

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
        self, payload: Dict[Any, Any]
    ) -> Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]:
        """verifies data before writting to destination also designs the destination file path

        Args:
            payload (Dict[Any, Any]):

        Raises:
            KeyError: if we do not find the exact keys we expect from the payload
            TypeError: if provided data object is not a list

        Returns:
            Tuple[str, Union[List[Dict[Any, Any]], Dict[Any, Any], Any]]: full destination path and
                                                                          data to be written
        """
        # confirm the payload keys are matching accurately with what is expected
        if not {"data", "date"}.issubset(set(payload.keys())):
            raise KeyError("Invalid payload ensure you have date and data as keys")

        if not re.search(r"\d{4}\-\d{2}\-\d{2}", payload["date"]):
            raise ValueError(
                "Invalid date format for partitioning expected: 'YYYY-mm-dd'"
            )
        if not isinstance(payload["data"], list):
            raise TypeError("Invalid data passed: expected List[Dict, Dict]")
        _date = payload["date"].replace("-", "")
        _data = payload["data"]
        write_path = f"{self.folder_path}/{_date}"
        return write_path, _data
