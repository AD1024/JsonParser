from tokenizer.Tokenizer import *
from tokenizer.TokenEnum import *
from tokenizer.TokenList import *
from tokenizer.Token import *
from model.JsonArray import JSONArray
from model.JsonObject import JSONObject

# Signal token
BEGIN_OBJECT = 1
BEGIN_ARRAY = 2
END_OBJECT = 4
END_ARRAY = 8

# variable token
NULL_TOKEN = 16
NUMBER_TOKEN = 32
STRING_TOKEN = 64
BOOL_TOKEN = 128

# separator token
COLON_TOKEN = 256
COMMA_TOKEN = 512

# end signal
END_JSON = 65536

class Parser(object) :

    def __init__(self, tokenList = TokenList()) :
        self.tokens = tokenList
    
    def __init__(self, data='') :
        self.tokens = Tokenizer(Reader(data)).getTokens()

    def parse(self) :
        token = self.tokens.next()
        if token == None :
            return JSONObject()
        elif token.getType() == TokenEnum.BEGIN_ARRAY :
            return self.parseJsonArray()
        elif token.getType() == TokenEnum.BEGIN_OBJECT :
            return self.parseJsonObject()
        else :
            raise ParseException('I')
    
    def checkToken(self, expected, actual) :
        if expected & actual == 0 :
            print(expected, actual)
            raise ParseException('T')

    def parseJsonArray(self) :
        expected = BEGIN_ARRAY | END_ARRAY | BEGIN_OBJECT | END_OBJECT | NULL_TOKEN | NUMBER_TOKEN | BOOL_TOKEN | STRING_TOKEN
        array = JSONArray()
        while self.tokens.hasNext() :
            token = self.tokens.next()
            tokenType = token.getType().value
            tokenValue = token.getValue()
            self.checkToken(expected, tokenType)

            if tokenType == BEGIN_OBJECT :
                array.append(self.parseJsonObject())
                expected = COMMA_TOKEN | END_ARRAY
            elif tokenType == BEGIN_ARRAY :
                array.append(self.parseJsonArray())
                expected = COMMA_TOKEN | END_ARRAY
            elif tokenType == END_ARRAY :
                return array
            elif tokenType == NULL_TOKEN :
                array.append(None)
                expected = COMMA_TOKEN | END_ARRAY
            elif tokenType == NUMBER_TOKEN :
                if tokenValue.__contains__('.') or tokenValue.__contains__('e') or tokenValue.__contains__('E') :
                    array.append(float(tokenValue))
                else :
                    array.append(int(tokenValue))
                expected = COMMA_TOKEN | END_ARRAY
            elif tokenType == STRING_TOKEN :
                array.append(tokenValue)
                expected = COMMA_TOKEN | END_ARRAY
            elif tokenType == BOOL_TOKEN :
                tokenValue = tokenValue.lower().capitalize()
                array.append({'True' : True, 'False': False}[tokenValue])
                expected = COMMA_TOKEN | END_ARRAY
            elif COMMA_TOKEN :
                expected = BEGIN_ARRAY | BEGIN_OBJECT | STRING_TOKEN | BOOL_TOKEN | NULL_TOKEN | NUMBER_TOKEN
            elif END_JSON :
                return array
            else :
                raise ParseException('U')
        raise ParseException('I')


    def parseJsonObject(self) :
        obj = JSONObject()
        expected = STRING_TOKEN | END_OBJECT
        key = None
        value = None
        while self.tokens.hasNext() :
            token = self.tokens.next()
            tokenType = token.getType().value
            tokenValue = token.getValue()
            self.checkToken(expected, tokenType)

            if tokenType == BEGIN_OBJECT :
                # chk(expected, tokenType)
                obj.put(key, self.parseJsonObject())
                expected = COMMA_TOKEN | END_OBJECT
            elif tokenType == END_OBJECT :
                # chk(expected, tokenType)
                return obj
            elif tokenType == BEGIN_ARRAY :
                # chk(expected, tokenType)
                obj.put(key, self.parseJsonArray())
                expected = COMMA_TOKEN | END_OBJECT
            elif tokenType == NULL_TOKEN :
                # chk(expected, tokenType)
                obj.put(key, None)
                expected = COMMA_TOKEN | END_OBJECT
            elif tokenType == STRING_TOKEN :
                preT = self.tokens.prevToken(2)
                # print(self.tokens.tokenList[self.tokens.cursor - 2])
                if preT.getType().value == COLON_TOKEN:
                    value = token.getValue()
                    obj.put(key, value)
                    expected = COMMA_TOKEN | END_OBJECT
                else :
                    key = token.getValue()
                    expected = COLON_TOKEN
            elif tokenType == NUMBER_TOKEN :
                if tokenValue.__contains__('.') or tokenValue.__contains__('e') or tokenValue.__contains__('E') :
                    obj.put(key, float(tokenValue))
                else :
                    obj.put(key, int(tokenValue))
                expected = COMMA_TOKEN | END_OBJECT
            elif tokenType == BOOL_TOKEN :
                tokenValue = tokenValue.lower().capitalize()
                obj.put(key, {'True' : True, 'False': False}[tokenValue])
                expected = COMMA_TOKEN | END_OBJECT
            elif tokenType == COLON_TOKEN :
                expected = NULL_TOKEN | NUMBER_TOKEN | BOOL_TOKEN | STRING_TOKEN | BEGIN_ARRAY | BEGIN_OBJECT
            elif tokenType == COMMA_TOKEN :
                expected = STRING_TOKEN
            elif tokenType == END_JSON :
                return obj
            else :
                raise ParseException('U')

        raise ParseException('I')                   