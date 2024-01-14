from datetime import datetime

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma, append_str
from ..Constants import CREDIT_CARD_SUFFIX
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.SbiCustomPdfParser import SbiCustomPdfParser


class SbiCcStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "SBI"
        self.source = source
        self.filepath = filepath
        config_name = append_str(self.name, CREDIT_CARD_SUFFIX)

        # Get data headers from config
        data_headers = config[config_name]['data_headers']
        data_header_list = []
        if data_headers:
            data_header_list = data_headers.split(",")

        self.parser = SbiCustomPdfParser(filepath, config[config_name][
            'record_selector_regex'], config[config_name]['igst_selector_regex'], data_header_list)

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
        sliced_amount = amount[0:len(amount) - 2]

        if amount and amount.endswith(' C'):
            debit_amount = None
            credit_amount = round(float(remove_comma(sliced_amount)), 2)
            closing_balance = credit_amount
        else:
            debit_amount = round(float(remove_comma(sliced_amount)), 2)
            credit_amount = None
            closing_balance = -debit_amount

        # Date formatting
        try:
            trans_date = datetime.strptime(value_dict['Date'], '%d %b %y')
        except ValueError:
            # Fallback on whole year format
            trans_date = datetime.strptime(value_dict['Date'], '%d %b %Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Transaction Details'],
            debit_amount,
            credit_amount,
            None,
            closing_balance,
            trans_date,
            None
        )

        return record
