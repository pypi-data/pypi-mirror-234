"""MODULE TO HELP WITH PROCESSING FILES"""
# pylint: disable=unused-argument, inconsistent-return-statements
from typing import Union, Dict, Any, Generator
from pathlib import Path
import json
from io import BytesIO
from io import TextIOWrapper
from csv import DictReader
from zipfile import ZipFile
from gzip import GzipFile
import yaml


def load_file(file_location: str, fmt: Union[str, None] = None) -> Dict[Any, Any]:
    """
    Gathers file data from json or yaml.
    """
    config: dict = {}
    if file_location.strip().rsplit(".", maxsplit=1)[-1] not in ["json", "yml", "yaml"]:
        raise TypeError("Wrong file type provided! Expecting only json and yaml files")

    file_location = str(file_location).strip()
    if file_location.endswith("yml"):
        with open(file_location, mode="r", encoding="utf8") as yaml_file:
            config = yaml.safe_load(yaml_file)
    if file_location.endswith("json"):
        with open(file_location, mode="r", encoding="utf8") as json_file:
            config = json.load(json_file)

    return config


def local_json_writer(
    payload: dict,
    filename: str,
    root_dir: str,
    folder_path: Union[str, None] = None,
    mode: str = "w",
) -> None:
    """WRITE DATA TO JSON OBJECT"""

    file_path = root_dir
    if folder_path:
        file_path = f"{root_dir}/{folder_path}"
        # CREATE FILE PATH IF NOT EXISTS
    Path(file_path).mkdir(parents=True, exist_ok=True)

    if filename is None or str(filename).strip() == "":
        raise ValueError("please proivde a destination filename")

    filename = f"{file_path}/{filename}.json"

    with open(f"{filename}", mode=mode, encoding="utf8") as dest_file:
        json.dump(payload, dest_file, indent=4)
        print(f"Done writting data to {filename}")

def parse_zip_to_csv(
    response, file_type: Union[str, None] = None
) -> Generator[Dict, None, None]:
    """Parse the zip file from api call"""
    if file_type == "zip":
        with ZipFile(BytesIO(response)) as zipfile:
            for file in zipfile.filelist:
                with zipfile.open(file) as file_contents:
                    dict_reader = DictReader(
                        TextIOWrapper(file_contents, encoding="utf-8")
                    )
                    yield from dict_reader
    elif file_type == "gzip":
        byte_object = BytesIO(response)
        byte_object.seek(0)
        with GzipFile(fileobj=byte_object, mode="r") as zipfile:
            dict_reader = DictReader(TextIOWrapper(zipfile, encoding="utf-8"))
            yield from dict_reader
