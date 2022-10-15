from decimal import Decimal
from datetime import datetime
from ..parser.DelimitedParserWithHeader import DelimitedParserWithHeader
from ..model.StatementDB import StatementDB


class HdfcDebitStatementProcessor:

    def __init__(self, filepath, source):
        self.name = "HDFC"
        self.source = source
        self.filepath = filepath
        self.parser = DelimitedParserWithHeader(filepath)

    def get_record(self):
        value_dict = self.parser.get_next_data()

        if value_dict == -1:
            # Reached end so closing file
            self.parser.close()
            return -1

        # Determine amount
        if Decimal(value_dict['Debit Amount']) > 0.00:
            debit_amount = float(value_dict['Debit Amount'])
            credit_amount = None
        else:
            debit_amount = None
            credit_amount = float(value_dict['Credit Amount'])

        # Date formatting
        trans_date = datetime.strptime(value_dict['Date'], '%d/%m/%y')
        value_date = datetime.strptime(value_dict['Value Dat'], '%d/%m/%y')

        record = StatementDB(
            self.name,
            self.source,
            trans_date,
            value_dict['Narration'],
            debit_amount,
            credit_amount,
            int(value_dict['Chq/Ref Number']),
            float(value_dict['Closing Balance']),
            value_date
        )

        return record
