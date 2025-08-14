import re

from pypdf import PdfReader

from .IParser import IParser
from ..logger import log


class PdfParserWithCustomHeader(IParser):

    def __init__(self, filename: str, record_selector_regex: str, record_end_regex: str, data_headers: list):
        self.record_selector_regex = record_selector_regex
        self.record_end_regex = record_end_regex
        self.data_headers = data_headers
        self.file_reader = PdfReader(filename)
        self.match_records = []
        self.index = 0

    def get_next_data(self):
        """
        Read and get single record in a dictionary from a pdf file.
        Will return -1 when it reaches end or end condition is met
        """
        key_value = {}

        # Calling only the First time to initialize match Records List
        if not self.match_records:
            self.__initialize_matched_records()

        if not self.match_records:
            return -1

        # Reached end of matched records
        if self.index >= len(self.match_records):
            return -1

        record = self.match_records[self.index]
        self.index = self.index + 1

        # Read and assign column from data_header
        match_group_num = 1
        for column_name in self.data_headers:
            key_value[column_name] = record.group(match_group_num)
            match_group_num = match_group_num + 1

        return key_value

    def __initialize_matched_records(self):
        log.info("Running Regex to initialize Match Records from pdf")
        number_of_pages = len(self.file_reader.pages)
        for i in range(0, number_of_pages):
            page = self.file_reader.pages[i]

            # Unexpected end of file or data_header not set
            if not page or not self.data_headers:
                return -1

            page_text = page.extract_text()
            matches = re.finditer(self.record_selector_regex, page_text, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                self.match_records.append(match)

            # End when regex matches the end condition if defined
            if self.record_end_regex:
                matchList = list(re.finditer(self.record_end_regex, page_text, re.MULTILINE))
                if matchList:
                    log.info("Reached end condition for record selection")
                    break

    def close(self):
        self.file_reader.stream.close()
