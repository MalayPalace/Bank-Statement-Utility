import xlrd

from .IParser import IParser
from ..logger import log


class XlsParserWithHeader(IParser):

    def __init__(self, filename: str, sheet_number: int, record_start_with: str):
        self.file = xlrd.open_workbook(filename, on_demand=True)
        self.sheet = self.file.sheet_by_index(sheet_number)

        if record_start_with:
            # As file reader starts from index 0
            self.record_start_with = int(record_start_with) - 1
        else:
            self.record_start_with = 0

        self.header = self.__get_header()

    def __get_header(self):
        headers = {}
        no_of_columns = self.sheet.ncols
        no_of_rows = self.sheet.nrows

        # check for end of file
        if self.record_start_with >= no_of_rows:
            log.error("File probably dont contain any Record")
            return -1

        row = self.sheet.row(self.record_start_with)
        self.record_start_with = self.record_start_with + 1

        if not row:
            return -1
        else:
            for col in range(0, no_of_columns):
                if row[col].value:
                    headers[col] = row[col].value.strip()

        return headers

    def get_next_data(self):
        """
        Read and get single record in a dictionary in a xls file.
        Will return -1 when it reaches end
        """
        key_value = {}
        no_of_rows = self.sheet.nrows

        # check for end of file
        if self.record_start_with >= no_of_rows:
            return -1

        row = self.sheet.row(self.record_start_with)
        # Unexpected end of file or data_header not set
        if not row or not self.header:
            return -1

        self.__add_values_with_data_header_moving_startpointer(key_value, row, self.header)
        return key_value

    def __add_values_with_data_header_moving_startpointer(self, key_value, row, data_header):
        # Read and assign column from data_header
        for column_num, column_name in data_header.items():
            key_value[column_name] = row[column_num].value
        self.record_start_with = self.record_start_with + 1

    def close(self):
        self.file.release_resources()
