import xlrd


class XlsParserWithCustomHeader:

    def __init__(self, filename: str, sheet_number: int, record_start_with: int, data_header_1: dict, data_header_2: dict):
        self.record_start_with = record_start_with
        self.data_header_1 = data_header_1
        self.data_header_2 = data_header_2
        self.file = xlrd.open_workbook(filename, on_demand=True)
        self.sheet = self.file.sheet_by_index(sheet_number)
        self.record_end_with = self.sheet.nrows

        self.__initialize_values()

    def __initialize_values(self):
        """
        Initializing values which are not passed and adjusting where needed.
        """
        if self.record_start_with:
            # As file reader starts from index 0
            self.record_start_with = int(self.record_start_with) - 1
        else:
            self.record_start_with = 0

    def get_next_data(self):
        """
        Read and get single record in a dictionary in a xls file.
        Will return -1 when it reaches end
        """
        key_value = {}

        # check for end of file
        if self.record_start_with >= self.record_end_with:
            return -1

        row = self.sheet.row(self.record_start_with)
        # Unexpected end of file or data_header not set
        if not row or not self.data_header_1:
            return -1

        self.__add_values_with_data_header_moving_startpointer(key_value, row, self.data_header_1)

        # If data header 2 is present then read process another row as data is spanning across 2 rows
        if self.data_header_2:
            row = self.sheet.row(self.record_start_with)
            # check for end of file
            if row and self.record_start_with < self.record_end_with:
                self.__add_values_with_data_header_moving_startpointer(key_value, row, self.data_header_2)

        return key_value

    def __add_values_with_data_header_moving_startpointer(self, key_value, row, data_header):
        # Read and assign column from data_header
        for column_num, column_name in data_header.items():
            key_value[column_name] = row[column_num - 1].value
        self.record_start_with = self.record_start_with + 1

    def close(self):
        self.file.release_resources()
