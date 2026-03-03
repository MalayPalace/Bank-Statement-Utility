from datetime import datetime

from .BankStatementInterface import BankStatementInterface
from .Utils import append_str, remove_comma
from ..Constants import CREDIT_CARD_SUFFIX
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.PdfParserWithCustomHeader import PdfParserWithCustomHeader


class HdfcCcStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "HDFC"
        self.source = source
        self.filepath = filepath
        config_name = append_str(self.name, CREDIT_CARD_SUFFIX)

        # Get data headers from config
        data_headers = config[config_name]['data_headers']
        data_header_list = []
        if data_headers:
            data_header_list = data_headers.split(",")

        self.parser = PdfParserWithCustomHeader(filepath, config[config_name][
            'record_selector_regex'], config[config_name]['record_end_regex'], data_header_list)

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1
        return value_dict

    def map_record(self, value_dict):
        # Determine amount
        amount = value_dict['Amount']

        credit_flag = value_dict['Credit']
        if credit_flag and credit_flag.strip() == '+':
            debit_amount = None
            credit_amount = round(float(remove_comma(amount)), 2)
            closing_balance = credit_amount
        else:
            debit_amount = round(float(remove_comma(amount)), 2)
            credit_amount = None
            closing_balance = -debit_amount

        # remove new lines character from description
        description = value_dict['Transaction Description'].replace('\n', '').strip()

        # Date formatting
        trans_date = datetime.strptime(value_dict['Date & Time'], '%d/%m/%Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            description,
            debit_amount,
            credit_amount,
            None,
            closing_balance,
            trans_date,
            None
        )

        return record
