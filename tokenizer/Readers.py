class Reader(object) :

    def __init__(self, string='') :
        self.data = string
        self.cursor = 0

    def size(self) :
        return len(self.data)

    def read(self, SIZE) :
        ret = ''
        if self.cursor == self.size() :
            return None
        cur = self.cursor
        if cur + SIZE + 1 < self.size() :
            ret =  self.data[cur:cur + SIZE + 1]
            cur += SIZE + 1
        else :
            ret = self.data[cur:]
            cur = self.size()
        self.cursor = cur
        return ret

class PosReader(object) :
    '''
        Segmental character reader
    '''

    def __init__(self, reader) :
        self.reader = reader
        self.data = ''
        self.cursor = 0
        self._BUFFER_SIZE = 1024
        self.requestData()

    # Request new data
    def requestData(self) :
        tmp = self.reader.read(self._BUFFER_SIZE)
        if tmp :
            self.data = tmp
            self.cursor = 0

    def currentPos(self) :
        if self.cursor - 1 >= len(self.data) :
            return None
        return self.data[max(0, self.cursor-1)]

    def nextPos(self) :
        if(self.hasNext()) :
            ret = self.data[self.cursor]
            self.cursor += 1
            return ret
        return None

    def prevPos(self) :
        self.cursor -= 1
        self.cursor = max(self.cursor, 0)
        
    def hasNext(self) :
        if self.cursor >= len(self.data) :
            self.requestData()
            if self.cursor > 0 :
                return False
            return True
        return True