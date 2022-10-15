import argparse
import datetime

from bank_statement_utility.config import config
from bank_statement_utility.logger import log
from bank_statement_utility.version import __version__
from bank_statement_utility.Constants import bank_names, account_type
from bank_statement_utility.parser.DelimitedParserWithHeader import DelimitedParserWithHeader
from bank_statement_utility.StatementProcessor import StatementProcessor

# def test_connectivity(filename):

    # reader = DelimitedParserWithHeader(filename)
    # data = reader.get_next_data()
    # print(data)
    # data = reader.get_next_data()
    # print(data)
    # reader.close()

#     statement_db = StatementDB('Sample', 'DebitCard', '2022-10-01', 'Sample UPI transaction-45 -value', 300.0, 'D', 0,
#                                500.0, '2022-10-01')
#     statement_db2 = StatementDB('Sample', 'DebitCard', '2022-10-03', 'Sample UPI transaction-5', 300.0, 'D', 0,
#                                500.0, '2022-10-02')
#     CassandraRepositoryHelper().insert_data(statement_db)
#     CassandraRepositoryHelper().insert_data(statement_db2)
#     CassandraRepositoryHelper().get_data()


def main():
    log.info('AppName, ' + config['Basic']['appName'])

    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-v", "--version", action='version', version=__version__)
    parser.add_argument("-n", "--name", help="Name of the bank", type=str.upper, choices=bank_names, required=True)
    parser.add_argument("-t", "--type", help="Type of account. Saving|Current|Creditcard", type=str.capitalize,
                        choices=account_type, required=True)
    parser.add_argument("filename", help="Bank Statement file to read")

    # Read arguments from command line
    args = parser.parse_args()

    bank_name = args.name
    source = args.type
    filename = args.filename

    #TODO Check file existing or not
    statement_processor = StatementProcessor(bank_name, source, filename)
    statement_processor.process()

    # test_connectivity(filename)


if __name__ == '__main__':
    main()
