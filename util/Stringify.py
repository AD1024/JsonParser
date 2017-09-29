def getIndent(dep) :
    ret = ''
    for i in range(0, dep * 2) :
        ret += ' '
    return ret

def arrayToString(array, dep) :
    from model.JsonArray import JSONArray
    from model.JsonObject import JSONObject
    ret = getIndent(dep)
    ret += '['
    dep += 1
    for i in range(0, array.size()) :
        ret += '\n'
        item = array.get(i)
        if isinstance(item, JSONArray) :
            ret += arrayToString(item, dep+1)
        elif isinstance(item, JSONObject) :
            ret += toString(item, dep+1)
        elif isinstance(item, str) :
            ret += getIndent();
            ret += '\"' + item + '\"'
        else :
            ret += getIndent(dep)
            ret += str(item)
        if i < array.size() - 1 :
            ret += ','
    dep -= 1
    ret += '\n'
    ret += getIndent(dep)
    ret += ']'
    return ret

def toString(obj, dep) :
    from model.JsonObject import JSONObject
    from model.JsonArray import JSONArray
    '''
    Stringify json data
    '''
    ret = getIndent(dep)
    ret += '{'
    dep += 1
    kvMap = obj.getAll()
    for i in range(0, len(kvMap)) :
        k = kvMap[i][0]
        v = kvMap[i][1]
        ret += '\n'
        ret += getIndent(dep)
        ret += '\"'
        ret += k
        ret += '\" :'
        if isinstance(v, JSONObject) :
            ret += '\n'
            ret += toString(v, dep+1)
        elif isinstance(v, JSONArray) :
            ret += '\n'
            ret += arrayToString(v, dep+1)
        elif isinstance(v, str) :
            ret += '\"' + v + '\"'
        else :
            ret += str(v)
        
        if i < len(kvMap) - 1 :
            ret += ','
    
    dep -= 1
    ret += '\n' + getIndent(dep)
    ret += '}'

    return ret