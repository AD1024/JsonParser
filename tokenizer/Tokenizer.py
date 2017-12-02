from ..exceptions.Exceptions import *
from .Readers import *
from .Token import *
from .TokenEnum import *
from .TokenList import *


class Tokenizer(object):
    def __init__(self, reader):
        self.ch = ''
        self.reader = PosReader(reader)
        self.tokenList = TokenList()
        self.tokenize()

    def get_tokens(self):
        return self.tokenList

    def tokenize(self):
        tk = self.parse()
        self.tokenList.append(tk)
        while tk.get_type() != TokenEnum.END_JSON:
            tk = self.parse()
            self.tokenList.append(tk)

    def parse(self):
        """Parse a string sequence"""
        self.ch = ''

        def is_space(char):
            return char in ('\n', '\t', '\r', ' ', '')

        def is_hex(char):
            return char.isdigit() or (ord(char) in range(ord('a'), ord('g'))) \
                   or (ord(char) in range(ord('A'), ord('G')))

        def is_exp(char):
            return char in ('e', 'E')

        def read():
            self.ch = self.reader.next_pos()

        def read_null():
            rem = self.reader.next_pos() + self.reader.next_pos() + self.reader.next_pos()
            if rem.lower() != 'ull':
                raise JsonTypeErrorException('null', 'n%s' % rem)
            else:
                return Token(TokenEnum.NULL, 'null')

        def read_bool(s):
            s = s.lower()
            if s == 't':
                rem = self.reader.next_pos() + self.reader.next_pos() + self.reader.next_pos()
            else:
                rem = self.reader.next_pos() + self.reader.next_pos() + self.reader.next_pos() + self.reader.next_pos()
            if rem.lower() != {'t': 'rue', 'f': 'alse'}[s]:
                raise JsonTypeErrorException({'t': 'true', 'f': 'false'}[s], s + rem)
            else:
                return Token(TokenEnum.BOOL, s + rem)

        def read_str():
            ret = ''
            while 1:
                read()
                if self.ch == '\\':
                    read()
                    '''
                    Temporarily remove escape test
                    if isEscape(self.ch) :
                        raise ParseException('I')
                    '''
                    ret += '\\'
                    self.ch = self.reader.current_pos()
                    ret += self.ch
                    if self.ch == 'u':
                        for i in (1, 2, 3, 4):
                            read()
                            if is_hex(self.ch):
                                ret += self.ch
                            else:
                                raise ParseException('I')
                    ret = str(ret)
                elif self.ch == '"':
                    tmp = self.reader.next_pos()
                    if tmp not in (']', '}', ',', ':', ' '):
                        self.ch += tmp
                        self.reader.prev_pos()
                    else:
                        self.reader.prev_pos()
                        return Token(TokenEnum.STRING, str(ret))
                elif self.ch == '\n' or self.ch == '\r':
                    ret += str(self.ch)
                else:
                    ret += str(self.ch)

        def read_exp():
            """
            Read an exp form of number
            :return:
            """
            ret = ''
            read()
            if self.ch == '+' or self.ch == '-':
                '''deal with numbers like 1e+3, 1e-10'''
                ret += self.ch
                read()
                if not self.ch.isdigit():
                    raise ParseException('E')
                ret += self.ch
                read()
                while self.ch.isdigit():
                    ret += self.ch
                    read()
                if self.ch:
                    '''
                    If the next character of the last of the number is not 
                    the end signal, the cursor should be moved one step back
                    '''
                    self.reader.prev_pos()
            else:
                '''deal with numbers like 1e10'''
                while self.ch.isdigit():
                    ret += self.ch
                    read()
                if self.ch:
                    self.reader.prev_pos()
                JsonTypeErrorException('e or E', self.ch)
            return ret

        def read_others():
            """
            Read other forms of values
            :return:
            """
            ret = ''
            prev_zero = self.ch == '0'
            read()
            if self.ch == '.':
                '''decimals'''
                ret += self.ch
                read()
                if not self.ch.isdigit():
                    raise ParseException('I')
                ret += self.ch
                read()
                while self.ch.isdigit():
                    ret += self.ch
                    read()
                if is_exp(self.ch):
                    ret += self.ch
                    ret += read_exp()
                else:
                    if self.ch:
                        self.reader.prev_pos()
            elif is_exp(self.ch):
                '''exp numbers'''
                ret += self.ch
                ret += read_exp()
            elif self.ch.lower() == 'x' and prev_zero:
                '''hex numbers'''
                ret += self.ch
                read()
                while is_hex(self.ch):
                    ret += self.ch
                    read()
                if self.ch:
                    self.reader.prev_pos()
            else:
                self.reader.prev_pos()
            return ret

        def read_num():
            ret = ''
            if self.ch == '-':
                ret += self.ch
                read()
                if self.ch == '0':
                    ret += self.ch
                    ret += read_others()
                elif ord(self.ch) in range(ord('1'), ord('9')+1):
                    ret += self.ch
                    read()
                    while self.ch and self.ch.isdigit():
                        ret += self.ch
                        read()
                    if self.ch:
                        self.reader.prev_pos()
                        ret += read_others()
                else:
                    raise ParseException('I')
            elif self.ch == '0':
                ret += '0'
                ret += read_others()
            else:
                ret += self.ch
                read()
                while self.ch and self.ch.isdigit():
                    ret += self.ch
                    read()
                if self.ch:
                    self.reader.prev_pos()
                    ret += read_others()
            return Token(TokenEnum.NUMBER, ret)

        while True:
            if self.reader.has_next():
                self.ch = self.reader.next_pos()
                if not is_space(self.ch):
                    break
            else:
                return Token(TokenEnum.END_JSON, None)
        if self.ch == '{':
            return Token(TokenEnum.BEGIN_OBJECT, self.ch)
        elif self.ch == '}':
            return Token(TokenEnum.END_OBJECT, self.ch)
        elif self.ch == '[':
            return Token(TokenEnum.BEGIN_ARRAY, self.ch)
        elif self.ch == ']':
            return Token(TokenEnum.END_ARRAY, self.ch)
        elif self.ch == ',':
            return Token(TokenEnum.COMMA, self.ch)
        elif self.ch == ':':
            return Token(TokenEnum.COLON, self.ch)
        elif self.ch == 'n':
            return read_null()
        elif self.ch.lower() == 't' or self.ch.lower() == 'f':
            return read_bool(self.ch)
        elif self.ch == '"':
            return read_str()
        elif self.ch == '-':
            return read_num()
        if self.ch.isdigit():
            return read_num()
