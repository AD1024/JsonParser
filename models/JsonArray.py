from .JsonObject import JSONObject
from ..exceptions.Exceptions import *
from ..util.Stringify import *


class JSONArray(list):
    def __init__(self):
        self.data = list()
        list.__init__(self.data)

    def size(self):
        return len(self.data)

    def get(self, i):
        return self.data[i]

    def append(self, i):
        self.data.append(i)

    def _parse_data(self, data):
        if type(data) == JSONObject:
            ret = {}
            for k, v in data.kvMap.items():
                ret.update({k: self._parse_data(v)})
            return ret
        elif type(data) == JSONArray:
            ret = []
            for i in data.data:
                ret.append(self._parse_data(i))
            return ret
        else:
            return data

    def to_python(self):
        return self._parse_data(self)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, value):
        self.data[i] = value

    def get_json_object(self, i):
        ret = self.data[i]
        if isinstance(ret, JSONObject):
            return ret
        raise JsonTypeErrorException('JSONObject', str(type(ret)))

    def get_json_array(self, i):
        ret = self.data[i]
        if isinstance(ret, JSONArray):
            return ret
        raise JsonTypeErrorException('JSONArray', str(type(ret)))

    def set_data(self, data):
        if type(data) == list:
            self.data = data.copy()
        else:
            raise TypeError('expected list, actual %s' % str(type(data)))

    def __repr__(self):
        return array_to_string(self, 0)

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __str__(self):
        return array_to_string(self, 0)

    def __iter__(self):
        return iter(self.data)

    def __eq__(self, array):
        if isinstance(array, JSONArray):
            if not self.size() == array.size():
                return False
            for i in range(0, self.size()):
                if not self.get[i] == array.get(i):
                    return False
            return True
        return False
