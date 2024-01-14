import argparse
import os
import sys
import time
from datetime import datetime, timedelta

from bank_statement_utility.Constants import bank_names, account_type
from bank_statement_utility.StatementProcessor import StatementProcessor
from bank_statement_utility.config import config
from bank_statement_utility.logger import log
from bank_statement_utility.services.ExportService import ExportService
from bank_statement_utility.services.VerificationService import VerificationService
from bank_statement_utility.version import __version__


def process():
    log.info(config['Basic']['appname'] + " version: " + __version__)

    # Initialize parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action='version', version=__version__)

    # subparsers for additional commands
    sub_parsers = parser.add_subparsers(title="commands", dest="command", help="Available Commands")

    # Save Command Parser
    save_sub_parser = sub_parsers.add_parser("save", help="Store Bank Statement")
    save_sub_parser.add_argument("-n", "--name", help="Name of the bank", type=str.upper, choices=bank_names,
                                 required=True)
    save_sub_parser.add_argument("-t", "--type", help="Type of account. Saving|Current|Creditcard", type=str.capitalize,
                                 choices=account_type, required=True)
    save_sub_parser.add_argument("filename", help="Bank Statement file to read")

    # Verify Command Parser
    verify_sub_parser = sub_parsers.add_parser("verify", help="Validation Command")
    verify_sub_parser.add_argument("-n", "--name", help="Name of the bank", type=str.upper, choices=bank_names,
                                   required=True)
    verify_sub_parser.add_argument("-t", "--type", help="Type of account. Saving|Current|Creditcard",
                                   type=str.capitalize,
                                   choices=account_type, required=True)
    verify_sub_parser.add_argument("--start-date",
                                   help="Start Date for verification command. Should follow DD-MM-YYYY format",
                                   type=str, required=False)

    # Export Command Parser
    sub_parsers.add_parser("export", help="Export Transaction sorted by latest Transaction Date")

    # Read arguments from command line
    args = parser.parse_args()

    cmd = args.command
    log.info(f"Using Command: {cmd}")

    # Start timer
    start_time = time.time()

    if cmd == "verify":
        # Read Variables from command-line
        bank_name = args.name
        source = args.type
        date_from_str = args.start_date

        if date_from_str:
            try:
                oldest_date = datetime.strptime(date_from_str, '%d-%m-%Y')
            except ValueError as ex:
                sys.exit(f"Date not in proper format: {ex}")
        else:
            years = 3
            no_of_days_in_year = 365
            oldest_date = datetime.now() - timedelta(days=years * no_of_days_in_year)

        print(f"Using Start Date:{oldest_date.date()}")
        verify_service = VerificationService(bank_name, source, oldest_date)
        result = verify_service.process()
        if result:
            print("Validation Successful!")
        else:
            print("Validation Failed!")
    elif cmd == "save":
        # Read Variables from command-line
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
    elif cmd == "export":
        ExportService().process()

    # Print Time taken
    print("--- Time Taken: %s seconds ---" % (time.time() - start_time))


# Main method to start execution from
def main():
    process()


if __name__ == '__main__':
    process()
