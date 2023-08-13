class StatementDB:

    def __init__(self, bank_name, source, transaction_date, description, debit_amount, credit_amount, ref_no, balance,
                 value_date, ins_date):
        self.bank_name = bank_name
        self.source = source
        self.transaction_date = transaction_date
        self.description = description
        self.debit_amount = debit_amount
        self.credit_amount = credit_amount
        if ref_no:
            self.cheque_ref_number = ref_no
        else:
            self.cheque_ref_number = "0"
        self.closing_balance = balance
        self.value_date = value_date
        if ins_date:
            self.ins_date = ins_date

    @staticmethod
    def to_instance(bank_name, source, transaction_date, description, debit_amount, credit_amount, ref_no,
                    balance, value_date, ins_date):
        statement = StatementDB(bank_name, source, transaction_date, description, debit_amount, credit_amount, ref_no,
                                balance, value_date, ins_date)
        # Round off amount field to 2 decimal places
        statement.closing_balance = round(float(statement.closing_balance), 2)
        if statement.debit_amount:
            statement.debit_amount = round(float(statement.debit_amount), 2)
        if statement.credit_amount:
            statement.credit_amount = round(float(statement.credit_amount), 2)
        return statement

    def __str__(self) -> str:
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
