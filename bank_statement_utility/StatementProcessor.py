from .services.HdfcDebitStatementProcessor import HdfcDebitStatementProcessor
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

        # Iterate over record and store to Cassandra. Stop when -1 is returned
        while (statement_model := processor.get_record()) != -1:
            log.debug("Saving Record: {record}".format(record=statement_model))
            self.cass_service.insert_data(statement_model)

        self.__close()

    def get_processor(self):
        log.info("Creating writer for {bank_name} bank and {source} source".format(bank_name=self.bank_name,
                                                                                   source=self.source))
        processor = None
        if self.bank_name == "HDFC":
            if self.source == "Saving" or self.source == "Current":
                processor = HdfcDebitStatementProcessor(self.filepath, self.source)

        return processor

    def __close(self):
        log.info("Closing database connection")
        self.cass_service.close_db()
