from ..util.Stringify import to_string


class JSONObject(dict):
    def __init__(self):
        self.kvMap = dict()
        dict.__init__(self.kvMap)

    def put(self, k, v):
        self.kvMap.update({k: v})

    def get(self, k, default=None):
        return self.kvMap.get(k, default)

    def get_all(self):
        return list(self.kvMap.items())

    def _parse_dict(self, data):
        from models.JsonArray import JSONArray
        if type(data) == JSONObject:
            ret = {}
            for k, v in data.kvMap.items():
                ret.update({k: self._parse_dict(v)})
            return ret
        elif type(data) == JSONArray:
            array = list()
            for i in data.data:
                array.append(self._parse_dict(i))
            return array
        else:
            return data

    def to_python(self):
        return self._parse_dict(self)

    def items(self):
        return self.kvMap.items()

    def keys(self):
        return self.kvMap.keys()

    def update(self, t):
        self.kvMap.update(t)

    def set_data(self, data):
        if type(data) == dict:
            if len(list(filter(lambda x: type(x) == str, data.keys()))) == len(data.keys()):
                self.kvMap = data.copy()
            else:
                raise TypeError('Unexpected type(s) of key(s)')
        else:
            raise TypeError('expected dict, actual %s' % str(type(data)))

    def __repr__(self):
        return to_string(self, 0)

    def __contains__(self, item):
        return self.kvMap.__contains__(item)

    def __str__(self):
        return to_string(self, 0)

    def __getitem__(self, key):
        return self.kvMap.get(key, None)

    def __setitem__(self, key, value):
        self.kvMap[key] = value

    def __iter__(self):
        return iter(self.kvMap)

    def __eq__(self, obj):
        if isinstance(obj, JSONObject):
            return self.kvMap == obj.kvMap
        return False
