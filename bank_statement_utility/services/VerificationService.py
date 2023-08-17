from .CassandraRepositoryHelper import CassandraRepositoryHelper
from ..logger import log


class VerificationService(object):

    def __init__(self, bank_name, source, transaction_date):
        self.bank_name = bank_name
        self.source = source
        self.transaction_date = transaction_date
        self.cass_service = CassandraRepositoryHelper()

    def process(self):
        result = self.cass_service.get_list_by_bank_and_source_ordered(self.bank_name, self.source,
                                                                       self.transaction_date)
        log.info("Validating for Bank:{bank} and Account Type:{source} and Start Transaction Date:{date}".format(
            bank=self.bank_name, source=self.source, date=self.transaction_date.date()))
        validate_flag = False

        if not result or not list(result):
            log.info("No Record Returned:{result}".format(result=result))
            print("No Record Returned")
            return validate_flag

        oldest_statement_row = result.__getitem__(0)
        newest_statement_row = result.__getitem__(len(result) - 1)

        log.debug(
            "Oldest Closing_balance:{closing_balance} Transaction Date:{trans_date} Debit/Credit:{debit_credit}".format(
                closing_balance=oldest_statement_row.closing_balance,
                trans_date=oldest_statement_row.transaction_date,
                debit_credit=-oldest_statement_row.debit_amount if oldest_statement_row.debit_amount else
                oldest_statement_row.credit_amount))
        log.debug(
            "Newest Closing_balance:{closing_balance} Transaction Date:{trans_date}".format(
                closing_balance=newest_statement_row.closing_balance,
                trans_date=newest_statement_row.transaction_date))

        # Total debit amount
        total_debit_amt = float(0)
        for row in result:
            if row.debit_amount:
                total_debit_amt = round(total_debit_amt + row.debit_amount, 2)
        log.debug("Total Debit Amount:{total_debit_amt}".format(total_debit_amt=total_debit_amt))

        # Total credit amount
        total_credit_amt = float(0)
        for row in result:
            if row.credit_amount:
                total_credit_amt = round(total_credit_amt + row.credit_amount, 2)
        log.debug("Total Credit Amount:{total_credit_amt}".format(total_credit_amt=total_credit_amt))

        diff_in_amount = self.__calculate_difference_of_balance(newest_statement_row, oldest_statement_row,
                                                                total_credit_amt, total_debit_amt)
        if diff_in_amount == 0:
            log.info("Successful")
            validate_flag = True
        else:
            log.info(f"Difference Found - Amount:{diff_in_amount}")
            print(f"Difference Found - Amount:{diff_in_amount}")

        # Close Db Connection
        log.info("Closing database connection")
        self.cass_service.close_db()

        return validate_flag

    @classmethod
    def __calculate_difference_of_balance(self, newest_statement_row, oldest_statement_row, total_credit_amt,
                                          total_debit_amt):
        closing_amt = float(oldest_statement_row.closing_balance)

        # Adjust oldest transaction debit/credit
        if oldest_statement_row.debit_amount:
            closing_amt = closing_amt + oldest_statement_row.debit_amount
        else:
            closing_amt = closing_amt - oldest_statement_row.credit_amount

        # Adjust total debit/credit
        closing_amt = round((closing_amt - total_debit_amt) + total_credit_amt, 2)
        log.debug(f"Total Calculated Amount:{closing_amt}")

        diff_in_amount = round(newest_statement_row.closing_balance - closing_amt, 2)
        return diff_in_amount
