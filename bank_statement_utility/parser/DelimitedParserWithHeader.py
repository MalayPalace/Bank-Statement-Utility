import io
from ..logger import log
import csv


class DelimitedParserWithHeader:
    """
    Delimited Parser which will consider first non-blank line as header and then all other lines as records.
    Will take care of blank lines at the start of the file.
    If record_start_with->str is passed it will treat that line as header and will continue with other
    lines as record till record_end_with(if passed) is found or blank line is found.
    If skip_data_column is passed it will skip that data column from reading, also it is non-zero based. Pass negative values if
    skipping particular column is not applicable.
    """

    def __init__(self, filename: str, record_start_with: str, record_end_with: str, skip_data_column: int):
        self.record_start_with = record_start_with
        self.record_end_with = record_end_with
        self.skip_data_column = skip_data_column
        self.file = io.open(filename, "rt", errors="ignore")
        self.header = self.__get_header()

    def __get_header(self):
        while not (line := self.file.readline().strip()):
            # truncating blank line
            line.strip()

        if self.record_start_with:
            while not line.startswith(self.record_start_with):
                line = self.file.readline().strip()

        line_array = line.split(",")
        return list(map(lambda l: l.strip(), line_array))  # stripping values across values

    def get_next_data(self):
        """
        Read and get single line in a dictionary in a delimited-header file.
        Will return -1 when it reaches end
        """
        key_value = {}

        line = self.file.readline()
        # check for end of file
        if not line.strip():
            return -1

        # end if record_end_with is specified and reached
        if self.record_end_with and line.startswith(self.record_end_with):
            log.debug("Found Record End with clause:" + self.record_end_with)
            return -1

        line_str = io.StringIO(line)
        values = list(csv.reader(line_str, delimiter=','))[0]  # As it is a single line

        i = 0
        for j in range(0, len(values)):
            # Skip those column specified in parser properties
            if self.skip_data_column <= 0 or j != self.skip_data_column:
                key_value[self.header[i]] = values[j].strip()
                i += 1

        return key_value

    def close(self):
        self.file.close()
