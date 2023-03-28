import argparse
import os
import sys
import time

from bank_statement_utility.Constants import bank_names, account_type
from bank_statement_utility.StatementProcessor import StatementProcessor
from bank_statement_utility.config import config
from bank_statement_utility.logger import log
from bank_statement_utility.version import __version__


def process():
    log.info(config['Basic']['appName'] + " version: " + __version__)

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

    is_file_exists = os.path.exists(filename)
    if not is_file_exists:
        log.error("File not found {path}".format(path=filename))
        sys.exit("No such File Exists. Exiting...")

    start_time = time.time()
    statement_processor = StatementProcessor(bank_name, source, filename)
    response = statement_processor.process()

    if response != 0:
        print("App ended with errors. Check logs for details")
    else:
        print("App ended successfully")
    print("--- Time Taken: %s seconds ---" % (time.time() - start_time))


# Main method to start execution from
def main():
    process()


if __name__ == '__main__':
    process()
