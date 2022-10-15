from cassandra.cluster import Cluster, PlainTextAuthProvider
from bank_statement_utility.logger import log
from bank_statement_utility.config import config
import datetime


class CassandraRepositoryHelper:
    __ins_user = "App"

    def __init__(self):
        contact_points = config['Cass']['contact.points']
        port = config['Cass']['port']
        username = config['Cass']['username']
        password = config['Cass']['password']

        self.cluster = Cluster(
            contact_points=[contact_points],
            port=port,
            protocol_version=4,
            auth_provider=PlainTextAuthProvider(username, password)
        )

        log.info("Creating session with host:{host}".format(host=contact_points + port))
        # Database Credentials
        self.session = self.cluster.connect()

    def get_data(self):
        result_set = self.session.execute("SELECT * FROM bank_statement.statement")
        value = result_set.all()
        print()
        if value:
            for v in value:
                print(value)
                print()
        else:
            print("Empty")

    def insert_data(self, data):
        stmt = self.session.prepare(
            "INSERT INTO bank_statement.statement(bank_name,source,transaction_date,description,debit_amount,credit_amount,"
            "closing_balance,cheque_ref_number,value_date,ins_date,ins_user) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        )

        query = stmt.bind([
            data.bank_name,
            data.source,
            data.transaction_date,
            data.description,
            data.debit_amount,
            data.credit_amount,
            data.closing_balance,
            data.cheque_ref_number,
            data.value_date,
            datetime.datetime.now(),
            self.__ins_user
        ])
        self.session.execute(query)
        log.debug("Query executed: " + query.__str__())

    def close_db(self):
        if self.cluster:
            self.cluster.shutdown()
