from datetime import datetime

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma, append_str
from ..Constants import CREDIT_CARD_SUFFIX
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.PdfParserWithCustomHeader import PdfParserWithCustomHeader


class KotakCcStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "KOTAK"
        self.source = source
        self.filepath = filepath
        config_name = append_str(self.name, CREDIT_CARD_SUFFIX)

        # Get data headers from config
        data_headers = config[config_name]['data_headers']
        data_header_list = []
        if data_headers:
            data_header_list = data_headers.split(",")

        self.parser = PdfParserWithCustomHeader(filepath, config[config_name][
            'record_selector_regex'], data_header_list)

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

        if amount and amount.endswith(' Cr'):
            debit_amount = None
            sliced_amount = amount[0:len(amount) - 3]
            credit_amount = round(float(remove_comma(sliced_amount)), 2)
        else:
            debit_amount = round(float(remove_comma(amount)), 2)
            credit_amount = None

        # Hard coding Closing Balance as its CreditCard
        closing_balance = 0.00

        # Date formatting
        trans_date = datetime.strptime(value_dict['Date'], '%d/%m/%Y')

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
