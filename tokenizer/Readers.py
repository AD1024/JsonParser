class Reader(object):
    def __init__(self, string=''):
        self.data = string
        self.cursor = 0

    def size(self):
        return len(self.data)

    def read(self, size):
        """
        Read a certain length of data
        :param size: the length expected to get
        :return: str: if size is greater than
        the remaining data, all the data will be returned, otherwise a string of length size will be returned
        """
        if self.cursor == self.size():
            return None
        cur = self.cursor
        if cur + size + 1 < self.size():
            ret = self.data[cur:cur + size + 1]
            cur += size + 1
        else:
            ret = self.data[cur:]
            cur = self.size()
        self.cursor = cur
        return ret


class PosReader(object):
    """
    Read only one character in each query
    """

    def __init__(self, reader):
        self.reader = reader
        self.data = ''
        self.cursor = 0
        self._BUFFER_SIZE = 1024
        self.request_data()

    # Request new data
    def request_data(self):
        """
        Request data from the ``Reader``
        :return: None
        """
        tmp = self.reader.read(self._BUFFER_SIZE)
        if tmp:
            self.data = tmp
            self.cursor = 0

    def current_pos(self):
        """
        Read the character at current position of the cursor
        :return: A single character or None if the cursor exceeds the maximum index
        """
        if self.cursor - 1 >= len(self.data):
            return None
        return self.data[max(0, self.cursor - 1)]

    def next_pos(self):
        """
        Move the cursor to the next position and then return the data cursor points to
        :return: A single character or None if the cursor exceeds the maximum index
        """
        if self.has_next():
            ret = self.data[self.cursor]
            self.cursor += 1
            return ret
        return None

    def prev_pos(self):
        """
        Move the cursor to previous position or do nothing if current position is 0
        :return: None
        """
        self.cursor -= 1
        self.cursor = max(self.cursor, 0)

    def has_next(self):
        """
        Check whether there is remaining data.
        If the cursor has reached the end, it will request new data from Reader.
        :return: True if there is remaining data either in ``PosReader`` or ``Reader``
        """
        if self.cursor >= len(self.data):
            self.request_data()
            if self.cursor > 0:
                return False
            return True
        return True
