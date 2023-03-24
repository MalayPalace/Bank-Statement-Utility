import argparse
import os
import sys
import ast

from bank_statement_utility.Constants import bank_names, account_type
from bank_statement_utility.StatementProcessor import StatementProcessor
from bank_statement_utility.config import config
from bank_statement_utility.logger import log
from bank_statement_utility.parser.XlsParserWithCustomHeader import XlsParserWithCustomHeader
from bank_statement_utility.version import __version__


def test_xls_parser():
    data_headers_1 = config['BOB']['data_headers1']
    data_headers_2 = config['BOB']['data_headers2']
    # converting string into dictionary
    data_header_1_dict = ast.literal_eval(data_headers_1)
    data_header_2_dict = ast.literal_eval(data_headers_2)

    record_start_with = config['BOB']['record_starts_with']

    log.info(data_header_1_dict)
    filename="sample-bob-xls.xls"
    xls_parser = XlsParserWithCustomHeader(filename, 0, record_start_with, data_header_1_dict, data_header_2_dict)

    iterable_flag = True
    while iterable_flag:
        values = xls_parser.get_next_data()
        log.info(values)
        if values == -1:
            iterable_flag = False

    log.info("Completed")

def main():

    log.info(config['Basic']['appName'] + " version: " + __version__)
    test_xls_parser()
    # # Initialize parser
    # parser = argparse.ArgumentParser()
    #
    # # Adding optional argument
    # parser.add_argument("-v", "--version", action='version', version=__version__)
    # parser.add_argument("-n", "--name", help="Name of the bank", type=str.upper, choices=bank_names, required=True)
    # parser.add_argument("-t", "--type", help="Type of account. Saving|Current|Creditcard", type=str.capitalize,
    #                     choices=account_type, required=True)
    # parser.add_argument("filename", help="Bank Statement file to read")
    #
    # # Read arguments from command line
    # args = parser.parse_args()
    #
    # bank_name = args.name
    # source = args.type
    # filename = args.filename
    #
    # is_file_exists = os.path.exists(filename)
    # if not is_file_exists:
    #     log.error("File not found {path}".format(path=filename))
    #     sys.exit("No such File Exists. Exiting...")
    #
    # statement_processor = StatementProcessor(bank_name, source, filename)
    # response = statement_processor.process()
    #
    # if response != 0:
    #     print("App ended successfully with errors. Check logs for details")
    # else:
    #     print("App ended successfully")


if __name__ == '__main__':
    main()
