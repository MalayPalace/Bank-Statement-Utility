CREATE KEYSPACE bank_statement WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE statement (
   bank_name text,
   source text,
   transaction_date date,
   description text,
   debit_amount decimal,
   credit_amount decimal,
   closing_balance decimal,
   cheque_ref_number text,
   value_date date,
   ins_date timestamp,
   ins_user text,
   Primary Key ((bank_name, source, transaction_date), description, closing_balance)
);
