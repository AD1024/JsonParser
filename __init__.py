__all__ = [
    'parse', 'prettify',
]

__author__ = 'Mike He <ccoderad@gmail.com>'

from .Parser import Parser
from .models.JsonObject import JSONObject
from .models.JsonArray import JSONArray


def parse(raw_data, use_python_data=True):
    return Parser.parse(raw_data, use_python_data)


def prettify(data):
    ret = Parser.parse(data, False)
    from .util.Stringify import to_string
    from .util.Stringify import array_to_string
    if isinstance(ret, JSONObject):
        return to_string(ret, 0)
    elif isinstance(ret, JSONArray):
        return array_to_string(ret, 0)
