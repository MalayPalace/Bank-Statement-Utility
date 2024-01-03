
class IParser:

    def get_next_data(self):
        """
        Get next record keeping the file open and parsing it.
        Return -1 incase unable to read any more records or it it is considered end as per the parser end condition

        """
        pass

    def close(self):
        pass
