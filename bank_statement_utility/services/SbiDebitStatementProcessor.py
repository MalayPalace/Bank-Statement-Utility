from datetime import datetime
from decimal import Decimal

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.XlsxParserWithHeader import XlsxParserWithHeader


class SbiDebitStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "SBI"
        self.source = source
        self.filepath = filepath
        self.parser = XlsxParserWithHeader(filepath, 0, config[self.name]['record_starts_with'])

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
        trans_date = datetime.strptime(value_dict['Date'], '%d/%m/%Y')

        # remove new lines character from description
        description = value_dict['Details'].replace('\n ', '').strip()
        # Fallback for description format without a space
        description = description.replace('\n', '').strip()

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            description,
            debit_amount,
            credit_amount,
            value_dict['Ref No/Cheque No'],
            closing_balance,
            trans_date,
            None
        )

        return record
