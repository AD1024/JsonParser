class JsonTypeErrorException(Exception):
    def __init__(self, expected='', actual=''):
        Exception.__init__(self, "JsonTypeError: Expected %s, Actual %s" % (expected, actual))


class JSONObjectKeyError(Exception):
    def __init__(self, msg='KeyError'):
        Exception.__init__(self, msg)


class ParseException(Exception):
    def __init__(self, msg='E'):
        msg_dict = {
            'E': 'ParseError',
            'T': 'TypeError',
            'I': 'Illegal Character',
            'T': 'Illegal Token',
            'U': 'Unexpected Token',
        }
        Exception.__init__(self, msg_dict.get(msg, msg))
