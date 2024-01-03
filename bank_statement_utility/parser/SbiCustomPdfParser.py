import re

from .PdfParserWithCustomHeader import PdfParserWithCustomHeader
from ..logger import log


class SbiCustomPdfParser(PdfParserWithCustomHeader):
    TRANSACTION_DATE_REGEX = '^for Statement dated ([0-9]{1,2} [A-Z][a-z]{2} [0-9]{4})'
    IGST_TRANS_REGEX = '^(IGST DB @ [0-9]{1,2}[.][0-9]{2}[%]) ([0-9,]+[.][0-9]{2} [DC])'

    def __init__(self, filename: str, record_selector_regex: str, data_headers: list):
        super().__init__(filename, record_selector_regex, data_headers)
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
                    log.debug('Swallowing Exception while searching IGST Transaction')
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
        date_match = re.finditer(self.TRANSACTION_DATE_REGEX, page_text, re.MULTILINE)
        transaction_date = next(date_match).group(1)

        # Get IGST Transaction
        igst_record_matches = re.finditer(self.IGST_TRANS_REGEX, page_text, re.MULTILINE)
        igst_record = next(igst_record_matches)
        key_value = {self.data_headers[0]: transaction_date, self.data_headers[1]: igst_record.group(1),
                     self.data_headers[2]: igst_record.group(2)}

        return key_value
