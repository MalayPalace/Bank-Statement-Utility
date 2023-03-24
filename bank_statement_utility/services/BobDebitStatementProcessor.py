import ast
from datetime import datetime

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.XlsParserWithCustomHeader import XlsParserWithCustomHeader


class BobDebitStatementProcessor(BankStatementInterface):
    def __init__(self, filepath, source):
        super().__init__()
        self.name = "BOB"
        self.source = source
        self.filepath = filepath

        # Get data headers from config
        data_headers_1 = config[self.name]['data_headers1']
        data_headers_2 = config[self.name]['data_headers2']

        # converting string into dictionary
        data_header_1_dict = ""
        data_header_2_dict = ""
        if data_headers_1:
            data_header_1_dict = ast.literal_eval(data_headers_1)
        if data_headers_2:
            data_header_2_dict = ast.literal_eval(data_headers_2)

        self.parser = XlsParserWithCustomHeader(filepath, 0, config[self.name]['record_starts_with'],
                                                data_header_1_dict, data_header_2_dict)

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1
        return value_dict

    def map_record(self, value_dict):
        # Determine amount
        amount = float(remove_comma(value_dict['Amount (INR)']))
        if amount >= 0.00:
            debit_amount = None
            credit_amount = amount
        else:
            debit_amount = abs(amount)
            credit_amount = None

        # format Closing Balance
        closing_balance = float(remove_comma(value_dict['Balance (INR)']))

        # Date formatting
        trans_date = datetime.strptime(value_dict['Date'], '%d/%m/%Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Description'],
            debit_amount,
            credit_amount,
            value_dict['Instrument ID'],
            closing_balance,
            trans_date
        )

        return record
