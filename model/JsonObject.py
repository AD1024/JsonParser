from util.Stringify import to_string


class JSONObject(dict):
    def __init__(self):
        self.kvMap = dict()
        dict.__init__(self.kvMap)

    def put(self, k, v):
        self.kvMap.update({k: v})

    def get(self, k):
        return self.kvMap.get(k, None)

    def get_all(self):
        return list(self.kvMap.items())

    def get_dict(self):
        return self.kvMap

    def __str__(self):
        return to_string(self, 0)

    def __getitem__(self, key):
        return self.kvMap.get(key, None)

    def __setitem__(self, key, value):
        self.kvMap[key] = value

    def __eq__(self, obj):
        if isinstance(obj, JSONObject):
            return self.kvMap == obj.kvMap
        return False
