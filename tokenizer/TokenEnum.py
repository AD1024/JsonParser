from enum import Enum


class TokenEnum(Enum):
    # Signal token
    BEGIN_OBJECT = 1
    BEGIN_ARRAY = 2
    END_OBJECT = 4
    END_ARRAY = 8

    # variable token
    NULL = 16
    NUMBER = 32
    STRING = 64
    BOOL = 128

    # separator token
    COLON = 256
    COMMA = 512

    # end signal
    END_JSON = 65536
