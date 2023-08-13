from datetime import datetime
from decimal import Decimal
from ..parser.DelimitedParserWithHeader import DelimitedParserWithHeader
from ..model.StatementDB import StatementDB
from .BankStatementInterface import BankStatementInterface
from ..config import config
from .Utils import remove_comma
from ..Constants import TAB


class SbiDebitStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "SBI"
        self.source = source
        self.filepath = filepath
        self.parser = DelimitedParserWithHeader(filepath, TAB, config[self.name]['record_starts_with'],
                                                "", -1)

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1
        return value_dict

    def map_record(self, value_dict):
        # Determine amount
        if value_dict['Debit'] and Decimal(remove_comma(value_dict['Debit'])) > 0.00:
            debit_amount = float(remove_comma(value_dict['Debit']))
            credit_amount = None
        else:
            debit_amount = None
            credit_amount = float(remove_comma(value_dict['Credit']))

        # format Closing Balance
        closing_balance = float(remove_comma(value_dict['Balance']))

        # Date formatting
        trans_date = datetime.strptime(value_dict['Txn Date'], '%d %b %Y')
        value_date = datetime.strptime(value_dict['Value Date'], '%d %b %Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Description'],
            debit_amount,
            credit_amount,
            value_dict['Ref No./Cheque No.'],
            closing_balance,
            value_date,
            None
        )

        return record
