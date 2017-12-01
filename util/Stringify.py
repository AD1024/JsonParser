def get_indent(dep):
    ret = ''
    for i in range(0, dep * 2):
        ret += ' '
    return ret


def array_to_string(array, dep):
    from ..models.JsonArray import JSONArray
    from ..models.JsonObject import JSONObject
    ret = get_indent(dep)
    ret += '['
    dep += 1
    for i in range(0, array.size()):
        ret += '\n'
        item = array.get(i)
        if isinstance(item, JSONArray):
            ret += array_to_string(item, dep + 1)
        elif isinstance(item, JSONObject):
            ret += to_string(item, dep + 1)
        elif isinstance(item, str):
            ret += get_indent(dep)
            ret += '\"' + item + '\"'
        else:
            ret += get_indent(dep)
            ret += str(item)
        if i < array.size() - 1:
            ret += ','
    dep -= 1
    ret += '\n'
    ret += get_indent(dep)
    ret += ']'
    return ret


def to_string(obj, dep):
    from ..models.JsonObject import JSONObject
    from ..models.JsonArray import JSONArray
    '''
    Stringify json data
    '''
    ret = get_indent(dep)
    ret += '{'
    dep += 1
    kv_map = obj.get_all()
    for i in range(0, len(kv_map)):
        k = kv_map[i][0]
        v = kv_map[i][1]
        ret += '\n'
        ret += get_indent(dep)
        ret += '\"'
        ret += k
        ret += '\" : '
        if isinstance(v, JSONObject):
            ret += '\n'
            ret += to_string(v, dep + 1)
        elif isinstance(v, JSONArray):
            ret += '\n'
            ret += array_to_string(v, dep + 1)
        elif isinstance(v, str):
            ret += '\"' + v + '\"'
        else:
            ret += str(v)

        if i < len(kv_map) - 1:
            ret += ','

    dep -= 1
    ret += '\n' + get_indent(dep)
    ret += '}'

    return ret
