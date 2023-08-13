from datetime import datetime
from decimal import Decimal

from .BankStatementInterface import BankStatementInterface
from .Utils import remove_comma
from ..Constants import COMMA
from ..config import config
from ..model.StatementDB import StatementDB
from ..parser.DelimitedParserWithHeader import DelimitedParserWithHeader


class KotakDebitStatementProcessor(BankStatementInterface):

    def __init__(self, filepath, source):
        self.name = "KOTAK"
        self.source = source
        self.filepath = filepath
        skip_data_col = int(config[self.name]['skip_data_column_no']) - 1
        self.parser = DelimitedParserWithHeader(filepath, COMMA, config[self.name]['record_starts_with'],
                                                config[self.name]['record_ends_with'], skip_data_col)

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
            debit_amount = round(float(remove_comma(value_dict['Debit'])), 2)
            credit_amount = None
        else:
            debit_amount = None
            credit_amount = round(float(remove_comma(value_dict['Credit'])), 2)

        # format Closing Balance
        closing_balance = round(float(remove_comma(value_dict['Balance'])), 2)

        # Date formatting
        trans_date = datetime.strptime(value_dict['Transaction Date'], '%d-%m-%Y')
        value_date = datetime.strptime(value_dict['Value Date'], '%d-%m-%Y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Description'],
            debit_amount,
            credit_amount,
            value_dict['Chq / Ref No.'],
            closing_balance,
            value_date,
            None
        )

        return record
