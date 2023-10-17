from ftplib import FTP
from io import BytesIO
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler


class FTPReader:
    """
    Custom FTP Reader
    """

    def __init__(self, creds_file, config_file):
        self._creds: dict = load_file(creds_file, "yml")

        self.config = load_file(config_file)

    @retry_handler(exceptions=TimeoutError, total_tries=5, initial_wait=900)
    def _query_handler(self) -> str:
        """
        Fetch XML from url
        """

        ftp = FTP(host=str(self.config.get("hostname")),
                  user=str(self._creds.get("user")),
                  passwd=str(self._creds.get("password")))

        ftp.encoding = "utf-8"
        read_io = BytesIO()

        try:
            ftp.retrbinary(f"RETR {self.config.get('filename')}", read_io.write)

        except Exception as err:
            raise err

        return read_io.getvalue().decode('utf8')

    def run_query(self) -> list:

        data = self._query_handler()

        # Split rows by newline
        data = data.split('\n')

        # Header is the first line
        headers = data[0].split('\t')

        # Last item is a timestamp
        lines = data[1:-1]

        # Split columns by tab
        list_of_lines = []
        for line in lines:
            list_of_lines.append(line.split('\t'))

        # Create list of dictionaries where the headers are the keys
        result = [dict(zip(headers, values)) for values in list_of_lines]

        return result
