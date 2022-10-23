import argparse

from bank_statement_utility.Constants import bank_names, account_type
from bank_statement_utility.StatementProcessor import StatementProcessor
from bank_statement_utility.config import config
from bank_statement_utility.logger import log
from bank_statement_utility.version import __version__


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

    # TODO Check file existing or not
    statement_processor = StatementProcessor(bank_name, source, filename)
    response = statement_processor.process()

    if response != 0:
        print("App ended successfully with errors. Check logs for details")
    else:
        print("App ended successfully")


if __name__ == '__main__':
    main()
