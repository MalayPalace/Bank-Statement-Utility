import csv

from .CassandraRepositoryHelper import CassandraRepositoryHelper
from ..logger import log


class ExportService(object):
    CSV_FILENAME = "combined_bank_statement.csv"
    QIF_FILENAME = "combined_bank_statement.qif"
    TABLE_FIELDS = ['Transaction Date', 'Bank Name', 'Account Type', 'Debit Amount', 'Credit Amount', 'Description',
                    'Closing Balance', 'Cheque Number']

    def __init__(self):
        self.cass_service = CassandraRepositoryHelper()

    def as_csv(self):
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

    def as_qif(self):
        result = self.cass_service.get_all_ordered_by_bank_latest()

        with open(self.QIF_FILENAME, mode='w', newline='') as qif_file:
            current_bank_source_name = None

            for statement in result:
                header = statement.bank_name + ("-Credit" if "Credit" in str(statement.source) else "")
                if header != current_bank_source_name:
                    current_bank_source_name = header
                    qif_file.write(f"!Account\nN{current_bank_source_name}\n")
                    qif_file.write("TBank\n^\n")
                    qif_file.write("!Type:Bank\n")

                qif_file.write("D{0}\n".format(statement.transaction_date))
                qif_file.write(
                    "T{0}\n".format(-statement.debit_amount if statement.debit_amount else statement.credit_amount))
                qif_file.write("P{0}\n".format(statement.description))
                qif_file.write("M{0}\n".format(statement.cheque_ref_number))
                qif_file.write("C\n")
                qif_file.write("^\n")

        log.info(f"Records Exported to file {self.QIF_FILENAME} Successfully")
        print(f"Records Exported to file {self.QIF_FILENAME} Successfully")
