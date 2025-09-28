import datetime
import sys

import pytz as pytz
from cassandra.cluster import Cluster, PlainTextAuthProvider, NoHostAvailable

from .Utils import is_ui_execution
from ..Constants import DB_TABLE_NAME
from ..config import config
from ..logger import log
from ..model.StatementDB import StatementDB


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

            if is_ui_execution():
                raise IOError("Unable to connect to DB. Check logs for more details")
            else:
                sys.exit("Unable to connect to DB. Check logs for more details. Exiting...")
        except Exception as err:
            log.error("Unknown error occur while connecting to DB. Error:{error}".format(error=err.__str__()),
                      exc_info=True)
            if is_ui_execution():
                raise IOError("Unknown error occur while connecting to DB. Check logs for more details.")
            else:
                sys.exit("Unknown error occur while connecting to DB. Check logs for more details. Exiting...")

    def insert_data(self, data):
        stmt = self.session.prepare(
            "INSERT INTO {0} (bank_name,source,transaction_date,description,debit_amount,credit_amount,closing_balance,"
            "cheque_ref_number,value_date,ins_date,ins_user) VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(
                DB_TABLE_NAME)
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
        # log.debug("Query executed: " + query.__str__())

    def get_list_by_bank_and_source_ordered(self, bank_name: str, source: str, transaction_date: datetime) -> (
            list)[StatementDB]:
        query = (
            "SELECT bank_name,source,transaction_date,description,debit_amount,credit_amount,closing_balance,ins_date "
            "FROM {0} "
            "WHERE bank_name = %s AND source = %s AND transaction_date >= %s ALLOW FILTERING;".format(
                DB_TABLE_NAME))

        # Convert the datetime to ISO 8601 format (string)
        iso_start_date = transaction_date.date().isoformat()

        # Execute and Convert the ResultSet to a list for sorting
        result = self.session.execute(query, [bank_name, source, iso_start_date])

        if result:
            # Define a custom sorting key function based on two columns
            def sorting_key(row):
                return row.transaction_date, row.ins_date

            # Sort the result list using the custom sorting key
            sorted_result = sorted(list(result), key=sorting_key)

            # Convert to StatementDb Object
            statement_obj = [StatementDB.to_instance(obj.bank_name, obj.source, obj.transaction_date, obj.description,
                                                     obj.debit_amount, obj.credit_amount, None, obj.closing_balance,
                                                     None, obj.ins_date) for
                             obj in sorted_result]
            return statement_obj

        return result

    def get_all_ordered_by_latest(self) -> list[StatementDB]:
        query = (
            "SELECT transaction_date,bank_name,source,debit_amount,credit_amount,description,closing_balance,cheque_ref_number,ins_date "
            "FROM {0}".format(
                DB_TABLE_NAME))

        # Execute and Convert the ResultSet to a list for sorting
        result = self.session.execute(query)

        if result:
            def sorting_key(row):
                return row.transaction_date

            # Sort the result list using the custom sorting key
            sorted_result = sorted(list(result), key=sorting_key, reverse=True)

            # Convert to StatementDb Object
            statement_obj = [StatementDB.to_instance(obj.bank_name, obj.source, obj.transaction_date, obj.description,
                                                     obj.debit_amount, obj.credit_amount, obj.cheque_ref_number,
                                                     obj.closing_balance,
                                                     None, obj.ins_date) for
                             obj in sorted_result]
            return statement_obj

        return result

    def get_all_ordered_by_bank_latest(self) -> list[StatementDB]:
        query = (
            "SELECT transaction_date,bank_name,source,debit_amount,credit_amount,description,closing_balance,"
            "cheque_ref_number,ins_date "
            "FROM {0}".format(DB_TABLE_NAME))
        result = self.session.execute(query)

        if result:
            sorted_result = sorted(list(result), key=lambda row: (row.bank_name, row.source, row.transaction_date),
                                   reverse=True)

            # Convert to StatementDb Object
            statement_obj = [StatementDB.to_instance(obj.bank_name, obj.source, obj.transaction_date, obj.description,
                                                     obj.debit_amount, obj.credit_amount, obj.cheque_ref_number,
                                                     obj.closing_balance,
                                                     None, obj.ins_date) for
                             obj in sorted_result]
            return statement_obj
        return result

    def get_min_max_date_by_bank_source_ordered(self) -> list[dict]:
        query = (
            "SELECT bank_name, source, transaction_date "
            "FROM {0}".format(DB_TABLE_NAME)
        )
        result = self.session.execute(query)
        agg = {}

        if result:
            for row in result:
                key = (row.bank_name, row.source)
                date = row.transaction_date
                if key not in agg:
                    agg[key] = {"bank_name": row.bank_name, "source": row.source, "min_date": date, "max_date": date}
                else:
                    if date < agg[key]["min_date"]:
                        agg[key]["min_date"] = date
                    if date > agg[key]["max_date"]:
                        agg[key]["max_date"] = date
            # Sort by max_date descending
            return sorted(agg.values(), key=lambda x: x["max_date"], reverse=True)

        return result

    def get_latest_balance(self, bank_name: str, source: str) -> float:
        query = (
            "SELECT closing_balance,transaction_date,ins_date "
            "FROM {0} "
            "WHERE bank_name = %s AND source = %s ALLOW FILTERING;".format(DB_TABLE_NAME)
        )
        result = self.session.execute(query, [bank_name, source])

        if result:
            sorted_result = sorted(list(result), key=lambda row: (row.transaction_date, row.ins_date), reverse=True)
            latest_balance = sorted_result[0].closing_balance
            return round(float(latest_balance), 2)

        return 0.0

    def get_outstanding_balance(self, bank_name: str, source: str) -> float:
        query = (
            "SELECT SUM(closing_balance) AS total_balance "
            "FROM {0} "
            "WHERE bank_name = %s AND source = %s ALLOW FILTERING;".format(DB_TABLE_NAME)
        )
        result = self.session.execute(query, [bank_name, source])
        row = result.one()

        if row and row.total_balance is not None:
            return round(float(row.total_balance), 2)

        return 0.0

    def close_db(self):
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
