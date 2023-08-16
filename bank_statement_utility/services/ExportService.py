import csv

from .CassandraRepositoryHelper import CassandraRepositoryHelper
from ..logger import log


class ExportService(object):
    CSV_FILENAME = "combined_bank_statement.csv"
    TABLE_FIELDS = ['Transaction Date', 'Bank Name', 'Account Type', 'Debit Amount', 'Credit Amount', 'Description',
                    'Closing Balance', 'Cheque Number']

    def __init__(self):
        self.cass_service = CassandraRepositoryHelper()

    def process(self):
        result = self.cass_service.get_all_ordered_by_latest()

        # Write the list of objects to the CSV file
        with open(self.CSV_FILENAME, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.TABLE_FIELDS)

            # Write the header row
            writer.writeheader()

            for statement in result:
                writer.writerow(
                    {self.TABLE_FIELDS[0]: statement.transaction_date, self.TABLE_FIELDS[1]: statement.bank_name,
                     self.TABLE_FIELDS[2]: statement.source, self.TABLE_FIELDS[3]: statement.debit_amount,
                     self.TABLE_FIELDS[4]: statement.credit_amount, self.TABLE_FIELDS[5]: statement.description,
                     self.TABLE_FIELDS[6]: statement.closing_balance,
                     self.TABLE_FIELDS[7]: statement.cheque_ref_number})

        log.info(f"Records Exported to file {self.CSV_FILENAME} Successfully")
        print(f"Records Exported to file {self.CSV_FILENAME} Successfully")
