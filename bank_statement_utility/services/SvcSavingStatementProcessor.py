from datetime import datetime

import xlrd

from .BankStatementInterface import BankStatementInterface
from ..config import config
from ..logger import log
from ..model.StatementDB import StatementDB
from ..parser.XlsParserWithHeader import XlsParserWithHeader


class SvcSavingStatementProcessor(BankStatementInterface):
    def __init__(self, filepath, source):
        super().__init__()
        self.name = "SVC"
        self.source = source
        self.filepath = filepath

        # Get value from config
        record_starts_with = config[self.name]['record_starts_with']

        self.parser = XlsParserWithHeader(filepath, 0, record_starts_with)

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1

        # Skipping Record Logic and call again
        if value_dict['Particulars'] == "By Opening Balance":
            log.info("Skipping record: {record}".format(
                record=value_dict
            ))
            value_dict = self.parser.get_next_data()
            if value_dict == -1:
                # Reached end so closing file
                self.parser.close()
                return -1

        return value_dict

    def map_record(self, value_dict):
        # Determine amount
        if value_dict['Debit']:
            debit_amount = float(value_dict['Debit'])
            credit_amount = None
        else:
            debit_amount = None
            credit_amount = float(value_dict['Credit'])

        # format Closing Balance
        closing_balance = float(value_dict['Balance'])

        # Date formatting
        try:
            trans_date = xlrd.xldate.xldate_as_datetime(value_dict['Date'], self.parser.file.datemode)
        except TypeError:
            # Fallback on String formatting
            trans_date = datetime.strptime(value_dict['Date'], '%d %b %Y')

        # Cheque no
        cheque_no = str(int(value_dict['Chq No.']))

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Particulars'],
            debit_amount,
            credit_amount,
            cheque_no,
            closing_balance,
            trans_date,
            None
        )

        return record
