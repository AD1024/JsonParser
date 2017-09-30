from exceptions.Exceptions import *
from .Readers import *
from .Token import *
from .TokenEnum import *
from .TokenList import *

class Tokenizer(object) :
    def __init__(self, reader) :
        self.reader = PosReader(reader)
        self.tokenList = TokenList()
        self.tokenize()

    def getTokens(self) :
        return self.tokenList
    
    def tokenize(self) :
        tk = None
        tk = self.parse()
        self.tokenList.append(tk)
        while tk.getType() != TokenEnum.END_JSON :
            tk = self.parse()
            # print(tk.getType())
            # print(tk.value)
            self.tokenList.append(tk)

    def parse(self) :
        self.ch = ''
        isSpace = lambda x : x in ('\n', '\t', '\r', ' ', '')
        isEscape = lambda x: x in ('"', 'u', 'r', 'n', 'b', 't', 'f', '\\')
        isHex = lambda x: x.isdigit() or (x >= 'a' and x <= 'f') or (x >= 'A' and x <= 'F')
        isExp = lambda x: x in ('e', 'E')
        
        def read() :
            self.ch = self.reader.nextPos()

        def readNull() :
            rem = self.reader.nextPos() + self.reader.nextPos() + self.reader.nextPos()
            if rem.lower() != 'ull' :
                raise JsonTypeErrorException('null', 'n%s' % rem)
            else :
                return Token(TokenEnum.NULL, 'null')

        def readBool(s) :
            s = s.lower()
            rem = ''
            if s == 't' :
                rem = self.reader.nextPos() + self.reader.nextPos() + self.reader.nextPos()
            else :
                rem = self.reader.nextPos() + self.reader.nextPos() + self.reader.nextPos() + self.reader.nextPos()
            if rem.lower() != {'t' : 'rue', 'f' : 'alse'}[s] :
                raise JsonTypeErrorException({'t' : 'true', 'f' : 'false'}[s], s + rem)
            else :
                return Token(TokenEnum.BOOL, s + rem)

        def readStr() :
            ret = ''
            while 1 :
                read()
                if self.ch == '\\' :
                    read()
                    '''
                    Temporarily remove escape test
                    if isEscape(self.ch) :
                        raise ParseException('I')
                    '''
                    ret += '\\'
                    self.ch = self.reader.currentPos()
                    ret += self.ch
                    if self.ch == 'u' :
                        for i in (1,2,3,4) :
                            read()
                            if isHex(self.ch) :
                                ret += self.ch
                            else :
                                raise ParseException('I')
                    ret = str(ret)
                elif self.ch == '"':
                    tmp = self.reader.nextPos()
                    if tmp not in (']', '}', ',', ':', ' ') :
                        self.ch += tmp
                        self.reader.prevPos()
                    else :
                        self.reader.prevPos()
                        return Token(TokenEnum.STRING, str(ret))
                elif self.ch == '\n' or self.ch == '\r' :
                    ret += str(self.ch)
                else :
                    ret += str(self.ch)

        def readExp() :
            ret = ''
            read()
            if self.ch == '+' or self.ch == '-' :
                ret += self.ch
                read()
                if not self.ch.isdigit() :
                    raise ParseException('E')
                ret += self.ch
                read()
                while self.ch.isdigit() :
                    ret += self.ch
                    read()
                if self.ch != None :
                    self.reader.prevPos()
            else :
                JsonTypeErrorException('e or E', self.ch)
            return ret

        def readOthers() :
            ret = ''
            read()
            if self.ch == '.' :
                ret += self.ch
                read()
                if not self.ch.isdigit() :
                    raise ParseException('I')
                ret += self.ch
                read()
                while self.ch.isdigit() :
                    ret += self.ch
                    read()
                if isExp(self.ch) :
                    ret += self.ch
                    ret += readExp()
                else :
                    if self.ch != None :
                        self.reader.prevPos()
            elif isExp(self.ch) :
                ret += self.ch
                ret += readExp()
            else :
                self.reader.prevPos()
            return ret

        def readNum() :
            ret = ''
            if self.ch == '-' :
                ret += self.ch
                read()
                if self.ch == '0' :
                    ret += self.ch
                    ret += readOthers()
                elif self.ch > '0' and self.ch <= '9' :
                    ret += self.ch
                    read()
                    while self.ch and self.ch.isdigit() :
                        ret += self.ch
                        read()
                    if self.ch != None :
                        self.reader.prevPos()
                        ret += readOthers()
                else :
                    raise ParseException('I')
            elif self.ch == '0' :
                ret += '0'
                ret += readOthers()
            else :
                ret += self.ch
                read()
                while self.ch and self.ch.isdigit() :
                    ret += self.ch
                    read()
                if self.ch != None :
                    self.reader.prevPos()
                    ret += readOthers()
            return Token(TokenEnum.NUMBER, ret)
        while True :
            if self.reader.hasNext() :
                self.ch = self.reader.nextPos()
                # print(self.ch)
                if not isSpace(self.ch) :
                    break
            else :
                return Token(TokenEnum.END_JSON, None)
        if self.ch == '{' :
            return Token(TokenEnum.BEGIN_OBJECT, self.ch)
        elif self.ch == '}' :
            return Token(TokenEnum.END_OBJECT, self.ch)
        elif self.ch == '[' :
            return Token(TokenEnum.BEGIN_ARRAY, self.ch)
        elif self.ch == ']' :
            return Token(TokenEnum.END_ARRAY, self.ch)
        elif self.ch == ',' :
            return Token(TokenEnum.COMMA, self.ch)
        elif self.ch == ':' :
            return Token(TokenEnum.COLON, self.ch)
        elif self.ch == 'n' :
            return readNull()
        elif self.ch.lower() == 't' or self.ch.lower() == 'f' :
            return readBool(self.ch)
        elif self.ch == '"' :
            return readStr()
        elif self.ch == '-' :
            return readNum()
        if self.ch.isdigit() :
            return readNum()
        