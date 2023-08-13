import ast
from datetime import datetime

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma
from ..Constants import SPACE
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.XlsParserWithCustomHeader import XlsParserWithCustomHeader


class IdbiDebitStatementProcessor(BankStatementInterface):
    def __init__(self, filepath, source):
        super().__init__()
        self.name = "IDBI"
        self.source = source
        self.filepath = filepath

        # Get data headers from config
        data_headers_1 = config[self.name]['data_headers1']

        # converting string into dictionary
        data_header_1_dict = ""
        if data_headers_1:
            data_header_1_dict = ast.literal_eval(data_headers_1)

        self.parser = XlsParserWithCustomHeader(filepath, 0, config[self.name]['record_starts_with'],
                                                data_header_1_dict, {})

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1
        return value_dict

    def map_record(self, value_dict):
        # Determine amount
        if value_dict['CR/DR'].upper() == "CR.":
            debit_amount = None
            credit_amount = round(float(remove_comma(value_dict['Amount (INR)'])), 2)
        else:
            debit_amount = round(float(remove_comma(value_dict['Amount (INR)'])), 2)
            credit_amount = None

        # format Closing Balance
        closing_balance = float(remove_comma(value_dict['Balance (INR)']))

        # Date formatting
        txn_date = value_dict['Txn Date'].split(SPACE)[0]
        try:
            trans_date = datetime.strptime(txn_date, '%d/%m/%Y')
        except ValueError:
            # Faced scenario where in IDBI was providing date in below format
            trans_date = datetime.strptime(txn_date, '%Y-%m-%d')

        value_date = datetime.strptime(value_dict['Value Date'], '%d/%m/%Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Description'],
            debit_amount,
            credit_amount,
            value_dict['Cheque No'],
            closing_balance,
            value_date,
            None
        )

        return record
