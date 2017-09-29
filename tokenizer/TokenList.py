class TokenList(object) :
    def __init__(self) :
        self.tokenList = list()
        self.cursor = 0

    def append(self, token) :
        self.tokenList.append(token)
    
    def next(self) :
        ret = self.tokenList[self.cursor]
        self.cursor += 1
        return ret

    def hasNext(self) :
        return self.cursor < len(self.tokenList)

    def currentToken(self) :
        if self.hasNext() :
            return self.tokenList[self.cursor]
        else :
            return None
    
    def prevToken(self, gen) :
        if self.cursor == 0 :
            return None
        return self.tokenList[self.cursor - gen]