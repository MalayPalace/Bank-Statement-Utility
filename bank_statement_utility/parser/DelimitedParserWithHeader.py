import io


class DelimitedParserWithHeader:

    def __init__(self, filename):
        self.file = io.open(filename, "rt", errors="ignore")
        self.header = self.__get_header()

    def __get_header(self):
        while not (line := self.file.readline().strip()):
            # truncating blank line
            line.strip()
        line_array = line.split(",")
        return list(map(lambda l: l.strip(), line_array))  # stripping values across values

    def get_next_data(self):
        """
        Read and get single line in a dictionary in a delimited-header file.
        Will return -1 when it reaches end
        """
        key_value = {}

        line = self.file.readline()
        # check for end of file
        if not line.strip():
            return -1

        values = line.split(",")

        i = 0
        for j in range(0, len(values)):
            key_value[self.header[i]] = values[j].strip()
            i += 1

        return key_value

    def close(self):
        self.file.close()
