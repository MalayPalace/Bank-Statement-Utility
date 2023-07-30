import sys

from .logger import log
from .services.BobDebitStatementProcessor import BobDebitStatementProcessor
from .services.CassandraRepositoryHelper import CassandraRepositoryHelper
from .services.HdfcDebitStatementProcessor import HdfcDebitStatementProcessor
from .services.IdbiDebitStatmentProcessor import IdbiDebitStatementProcessor
from .services.KotakDebitStatementProcessor import KotakDebitStatementProcessor
from .services.SbiDebitStatementProcessor import SbiDebitStatementProcessor
from .services.SvcSavingStatementProcessor import SvcSavingStatementProcessor


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
            # Counter to check if it was unable to parse file correctly
            track_count = 0
            while iterable_flag:
                try:
                    record = processor.get_record()
                    if record != -1:
                        statement_model = processor.map_record(record)
                        log.debug("Saving Record: {record}".format(record=statement_model))
                        self.cass_service.insert_data(statement_model)
                        track_count = track_count + 1
                    else:
                        if track_count == 0:
                            log.warn("File contain invalid record or parser was not able to parse file correctly")
                            print("File contains invalid record or parser was not able to parse file correctly")
                        iterable_flag = False

                except AttributeError as err:
                    log.error("Error while conversion of Record {record}".format(record=record))
                    log.error("AttributeError {error} ".format(error=err.__str__()), exc_info=True)
                    failed_records.append(record)
                except Exception as err:
                    log.error("Unknown Error occurred {error} ".format(error=err.__str__()), exc_info=True)
                    failed_records.append(record)

            if failed_records:
                self.log_fail_records(failed_records)
            else:
                response = 0
            log.info("Records Processed: " + str(track_count))
            # Also printing to std output
            print("Records Processed: " + str(track_count))
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
        elif self.bank_name == "IDBI":
            if self.source == "Saving" or self.source == "Current":
                processor = IdbiDebitStatementProcessor(self.filepath, self.source)
        elif self.bank_name == "SVC":
            if self.source == "Saving" or self.source == "Current":
                processor = SvcSavingStatementProcessor(self.filepath, self.source)

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
