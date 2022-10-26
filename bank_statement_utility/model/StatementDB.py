class StatementDB:

    def __init__(self, bank_name, source, transaction_date, description, debit_amount, credit_amount, ref_no, balance,
                 value_date):
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

    def __str__(self) -> str:
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
