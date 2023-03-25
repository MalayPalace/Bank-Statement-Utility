import datetime
import sys

import pytz as pytz
from cassandra.cluster import Cluster, PlainTextAuthProvider, NoHostAvailable

from bank_statement_utility.config import config
from bank_statement_utility.logger import log


class CassandraRepositoryHelper:
    __ins_user = "App"
    __IST_TIMEZONE = pytz.timezone('Asia/Kolkata')

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
        try:
            self.session = self.cluster.connect()
        except NoHostAvailable:
            log.error("Unable to connect to DB on {host}:{port} with user:{user}. DB host not available".format(
                host=contact_points,
                port=port, user=username))
            sys.exit("Unable to connect to DB. Check logs for more details. Exiting...")
        except Exception as err:
            log.error("Unknown error occur while connecting to DB. Error:{error}".format(error=err.__str__()),
                      exc_info=True)
            sys.exit("Unknown error occur while connecting to DB. Check logs for more details. Exiting...")

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
            datetime.datetime.now(tz=self.__IST_TIMEZONE),
            self.__ins_user
        ])
        self.session.execute(query)
        log.debug("Query executed: " + query.__str__())

    def close_db(self):
        if self.cluster:
            self.cluster.shutdown()
