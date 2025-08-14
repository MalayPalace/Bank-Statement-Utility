import re

from .PdfParserWithCustomHeader import PdfParserWithCustomHeader
from ..Constants import EMPTY_STRING
from ..logger import log


class SbiCustomPdfParser(PdfParserWithCustomHeader):

    def __init__(self, filename: str, record_selector_regex: str, igst_selector_regex: str, igst_date_regex: str,
                 data_headers: list):
        super().__init__(filename, record_selector_regex, EMPTY_STRING, data_headers)
        self.igst_selector_regex = igst_selector_regex
        self.igst_date_regex = igst_date_regex
        self.returned_igst_record = False

    def get_next_data(self):
        value_dict = super().get_next_data()

        if value_dict == -1:

            # Additional Handling for IGST Charge Transaction
            if not self.returned_igst_record:
                self.returned_igst_record = True
                try:
                    record = self.__get_igst_transaction()
                    if record:
                        return record
                except Exception:
                    log.info('Swallowing Exception while searching IGST Transaction', exc_info=True)
            else:
                return -1

        return value_dict

    def __get_igst_transaction(self):
        page = self.file_reader.pages[0]

        # Unexpected end of file or data_header not set
        if not page or not self.data_headers:
            return -1

        page_text = page.extract_text()

        # Get Transaction date
        date_match = re.finditer(self.igst_date_regex, page_text, re.MULTILINE)
        transaction_date = next(date_match).group(1)

        # Get IGST Transaction
        igst_record_matches = re.finditer(self.igst_selector_regex, page_text, re.MULTILINE)
        igst_record = next(igst_record_matches)
        key_value = {self.data_headers[0]: transaction_date, self.data_headers[1]: igst_record.group(1),
                     self.data_headers[2]: igst_record.group(2)}

        return key_value
