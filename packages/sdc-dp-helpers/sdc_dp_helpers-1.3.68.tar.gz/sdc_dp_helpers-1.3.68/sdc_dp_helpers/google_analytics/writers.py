"""CUSTOM MODULE TO WRITE GA DATA"""
# pylint: disable=too-few-public-methods, too-many-arguments
from typing import Union, List, Any, Dict, Tuple, Optional
from sdc_dp_helpers.base_writers import BaseWriter


class GAV3Writer(BaseWriter):
    """WRITER FOR GA V3 DATA"""

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
        """
        This pulls the yielded dataset from the GA reader in a manner
        that consumes the dataset of the given view_id and date,
        and writes it to s3 so that duplication does not occur.
        :param payload: This is a key value object that looks like:
                        {
                            "data": list(),
                            "date": string,
                            "view_id": string
                        }
        """
        if list(payload.keys()).sort() != ["data", "date", "view_id"].sort():
            raise KeyError("Invalid payload")
        if not isinstance(payload["data"], list):
            raise TypeError("invalid data passed: expected List[Dict[Any,Any]]")
        if not isinstance(payload["view_id"], str):
            raise TypeError("invalid view_id passed: expected string")
        _view_id= payload.get("view_id")
        _date = payload.get("date")
        if _date:
            _date = _date.replace("-", "")
        else:
            raise KeyError("Date cannot be None")
        _data = payload.get("data")
        write_path: str = f"{self.folder_path}/{_view_id}/{_date}"

        return write_path, _data
