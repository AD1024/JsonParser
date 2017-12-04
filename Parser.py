from .models.JsonArray import JSONArray

from .models.JsonObject import JSONObject
from .tokenizer.Tokenizer import *

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


class Parser(object):
    __slots__ = ('tokens',)

    @classmethod
    def parse(cls, data=None, use_built_in=True):
        """
        Parse the json data provided
        :param data: data can be ``str`` or ``TokenList``, which comes from ``Tokenizer``
        :param get_python_data: return PythonObj if True else JSON data(JSONObject/JSONArray)
        :return: JSONObject or JSONArray
        """
        cls.data_conf = use_built_in
        if type(data) == str:
            cls.tokens = Tokenizer(Reader(data)).get_tokens()
        elif type(data) == TokenList:
            cls.tokens = data
        elif not data:
            return JSONObject()
        return cls._work()

    @classmethod
    def _work(cls):
        """
        Major parsing function
        :return: JSONObject or JSONArray
        """
        token = cls.tokens.next()
        if not token:
            return JSONObject()
        elif token.get_type() == TokenEnum.BEGIN_ARRAY:
            return cls.parse_json_array()
        elif token.get_type() == TokenEnum.BEGIN_OBJECT:
            return cls.parse_json_object()
        else:
            raise ParseException('Illegal token at beginning')

    @classmethod
    def check_token(cls, expected, actual):
        """
        Check whether set expected and set actual have intersections(Bit mask).
        For instance is the `expected` token is `END_OBJECT` or `COMMA_TOKEN`, which is 4(100) and 512(1000000000)
        the `expected` will be 1000000100.
        :param expected: the expected set of tokens
        :param actual: current token got from parser
        :return: True if actual token is one element in `expected` otherwise False will be returned
        """
        if expected & actual == 0:
            raise ParseException('Unexpected Token at position %d' % cls.tokens.get_cursor_position())

    @classmethod
    def get_text(cls, data):
        """
        Decode the string in order to process unicode data in order to make convenience while parsing Chinese data
        :param data: raw string
        :return: decoded string
        """
        return data.encode('utf-8').decode('unicode-escape')

    @classmethod
    def parse_json_array(cls):
        """ Parse a JSONArray"""
        expected = BEGIN_ARRAY | END_ARRAY | BEGIN_OBJECT | END_OBJECT | \
                        NULL_TOKEN | NUMBER_TOKEN | BOOL_TOKEN | STRING_TOKEN
        array = {False: JSONArray(), True: list()}.get(cls.data_conf)
        while cls.tokens.has_next():
            token = cls.tokens.next()
            # token_type -> TokenEnum
            token_type = token.get_type().value
            token_value = token.get_value()
            cls.check_token(expected, token_type)

            # check through each condition
            if token_type == BEGIN_OBJECT:
                array.append(cls.parse_json_object())
                expected = COMMA_TOKEN | END_ARRAY
            elif token_type == BEGIN_ARRAY:
                array.append(cls.parse_json_array())
                expected = COMMA_TOKEN | END_ARRAY
            elif token_type == END_ARRAY:
                return array
            elif token_type == NULL_TOKEN:
                array.append(None)
                expected = COMMA_TOKEN | END_ARRAY
            elif token_type == NUMBER_TOKEN:
                if '.' in token_value or 'e' in token_value or 'E' in token_value:
                    array.append(float(token_value))
                elif 'x' in token_value:
                    array.append(int(token_value, base=16))
                else:
                    array.append(int(token_value))
                expected = COMMA_TOKEN | END_ARRAY
            elif token_type == STRING_TOKEN:
                array.append(token_value)
                expected = COMMA_TOKEN | END_ARRAY
            elif token_type == BOOL_TOKEN:
                token_value = token_value.lower().capitalize()
                array.append({'True': True, 'False': False}[token_value])
                expected = COMMA_TOKEN | END_ARRAY
            elif COMMA_TOKEN:
                expected = BEGIN_ARRAY | BEGIN_OBJECT | STRING_TOKEN | BOOL_TOKEN | NULL_TOKEN | NUMBER_TOKEN
            elif END_JSON:
                return array
            else:
                raise ParseException('Unexpected token at position %d' % cls.tokens.get_cursor_position())
        raise ParseException('Illegal token at position %d' % cls.tokens.get_cursor_position())

    @classmethod
    def parse_json_object(cls):
        """Parse a JSONObject"""
        obj = {False: JSONObject(), True: dict()}.get(cls.data_conf)
        expected = STRING_TOKEN | END_OBJECT
        key = None
        while cls.tokens.has_next():
            token = cls.tokens.next()
            token_type = token.get_type().value
            token_value = token.get_value()
            cls.check_token(expected, token_type)

            if token_type == BEGIN_OBJECT:
                obj.update({key: cls.parse_json_object()})
                expected = COMMA_TOKEN | END_OBJECT
            elif token_type == END_OBJECT:
                return obj
            elif token_type == BEGIN_ARRAY:
                obj.update({key: cls.parse_json_array()})
                expected = COMMA_TOKEN | END_OBJECT
            elif token_type == NULL_TOKEN:
                obj.update({key: None})
                expected = COMMA_TOKEN | END_OBJECT
            elif token_type == STRING_TOKEN:
                pre_token = cls.tokens.prev_token(2)
                if pre_token.get_type().value == COLON_TOKEN:
                    value = token.get_value()
                    obj.update({key: value})
                    expected = COMMA_TOKEN | END_OBJECT
                else:
                    key = token.get_value()
                    # if obj.__contains__(key):
                    #    raise KeyError('Duplicated key: {}'.format(key))
                    expected = COLON_TOKEN
            elif token_type == NUMBER_TOKEN:
                if '.' in token_value or 'e' in token_value or 'E' in token_value:
                    obj.update({key: float(token_value)})
                elif 'x' in token_value:
                    obj.update({key: int(token_value, base=16)})
                else:
                    obj.update({key: int(token_value)})
                expected = COMMA_TOKEN | END_OBJECT
            elif token_type == BOOL_TOKEN:
                token_value = token_value.lower().capitalize()
                obj.update({key: {'True': True, 'False': False}[token_value]})
                expected = COMMA_TOKEN | END_OBJECT
            elif token_type == COLON_TOKEN:
                expected = NULL_TOKEN | NUMBER_TOKEN | BOOL_TOKEN | STRING_TOKEN | BEGIN_ARRAY | BEGIN_OBJECT
            elif token_type == COMMA_TOKEN:
                expected = STRING_TOKEN
            elif token_type == END_JSON:
                return obj
            else:
                raise ParseException('Unexpected token at position %d' % cls.tokens.get_cursor_position())

        raise ParseException('Illegal token at position %d' % cls.tokens.get_cursor_position())
