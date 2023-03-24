import sys

from .services.HdfcDebitStatementProcessor import HdfcDebitStatementProcessor
from .services.KotakDebitStatementProcessor import KotakDebitStatementProcessor
from .services.SbiDebitStatementProcessor import SbiDebitStatementProcessor
from .services.BobDebitStatementProcessor import BobDebitStatementProcessor
from .services.CassandraRepositoryHelper import CassandraRepositoryHelper
from .logger import log


class StatementProcessor(object):

    def __init__(self, bank_name, source, filepath):
        self.bank_name = bank_name
        self.source = source
        self.filepath = filepath
        self.cass_service = CassandraRepositoryHelper()

    def process(self):
        # create processor
        processor = self.get_processor()

        response = -1
        if processor:
            # Iterate over record and store to Cassandra. Stop when -1 is returned
            iterable_flag = True
            record = -1

            failed_records = []

            while iterable_flag:
                try:
                    record = processor.get_record()
                    if record != -1:
                        statement_model = processor.map_record(record)
                        log.debug("Saving Record: {record}".format(record=statement_model))
                        self.cass_service.insert_data(statement_model)
                    else:
                        # TODO: If it returns -1 in the very first loop, send out valid error message that
                        #  file dont contain any valid record or not able to parse file correctly
                        iterable_flag = False
                except AttributeError:
                    log.error("Error while conversion of Record {record}".format(record=record))
                    failed_records.append(record)
                except Exception as err:
                    log.error("Unknown Error occurred {error} ".format(error=err.__str__()), exc_info=True)
                    failed_records.append(record)

            if failed_records:
                self.log_fail_records(failed_records)
            else:
                response = 0
        else:
            log.error("No Processor defined for bank {bank_name} and source type {source}".format(bank_name=self.bank_name,
                                                                                                  source=self.source))
            self.__close()
            sys.exit("No processor found for given bank-name and source. Check logs for more details. Exiting...")

        self.__close()
        return response

    def get_processor(self):
        log.info("Creating writer for {bank_name} bank and {source} source".format(bank_name=self.bank_name,
                                                                                   source=self.source))
        processor = None
        if self.bank_name == "HDFC":
            if self.source == "Saving" or self.source == "Current":
                processor = HdfcDebitStatementProcessor(self.filepath, self.source)
        elif self.bank_name == "KOTAK":
            if self.source == "Saving" or self.source == "Current":
                processor = KotakDebitStatementProcessor(self.filepath, self.source)
        elif self.bank_name == "SBI":
            if self.source == "Saving" or self.source == "Current":
                processor = SbiDebitStatementProcessor(self.filepath, self.source)
        elif self.bank_name == "BOB":
            if self.source == "Saving" or self.source == "Current":
                processor = BobDebitStatementProcessor(self.filepath, self.source)

        return processor

    def log_fail_records(self, failed_records):
        if failed_records:
            log.warn("*********Below records failed while executing file:{file}*****".format(file=self.filepath))
            for fail_record in failed_records:
                log.warn(fail_record)

            log.warn("*********End*****")

    def __close(self):
        log.info("Closing database connection")
        self.cass_service.close_db()
