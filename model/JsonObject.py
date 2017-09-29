from util.Stringify import toString

class JSONObject(dict) :
    def __init__(self) :
        self.kvMap = dict()
    
    def put(self, K, V) :
        self.kvMap.update({K : V})
    
    def get(self, K) :
        return self.kvMap.get(K)

    def getAll(self) :
        return list(self.kvMap.items())

    def __str__(self) :
        return toString(self, 0)

    def __getitem__(self, key) :
        return self.kvMap.get(key, None)
    
    def __setitem__(self, key, value) :
        self.kvMap[key] = value

    def __eq__(self, obj) :
        if isinstance(obj, JSONObject) :
            return self.kvMap == obj.kvMap
        return False