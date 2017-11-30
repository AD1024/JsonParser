class Reader(object):
    def __init__(self, string=''):
        self.data = string
        self.cursor = 0

    def size(self):
        return len(self.data)

    def read(self, size):
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
    '''
        Segmental character reader
    '''

    def __init__(self, reader):
        self.reader = reader
        self.data = ''
        self.cursor = 0
        self._BUFFER_SIZE = 1024
        self.request_data()

    # Request new data
    def request_data(self):
        tmp = self.reader.read(self._BUFFER_SIZE)
        if tmp:
            self.data = tmp
            self.cursor = 0

    def current_pos(self):
        if self.cursor - 1 >= len(self.data):
            return None
        return self.data[max(0, self.cursor - 1)]

    def next_pos(self):
        if self.has_next():
            ret = self.data[self.cursor]
            self.cursor += 1
            return ret
        return None

    def prev_pos(self):
        self.cursor -= 1
        self.cursor = max(self.cursor, 0)

    def has_next(self):
        if self.cursor >= len(self.data):
            self.request_data()
            if self.cursor > 0:
                return False
            return True
        return True
