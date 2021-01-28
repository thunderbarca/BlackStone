import json


def jsonXssFilter(data):
    payloads = {
        '\'': '&apos;',
        '"': '&quot;',
        '<': '&lt;',
        '>': '&gt;'
    }
    if type(data) == dict:
        new = {}
        for key, values in data.items():
            new[key] = jsonXssFilter(values)
    elif type(data) == list:
        new = []
        for i in data:
            new.append(jsonXssFilter(i))
    elif type(data) == int or type(data) == float:
        new = data
    elif type(data) == str:
        new = data
        for key, value in payloads.items():
            new = new.replace(key, value)
    elif type(data) == bytes:
        new = data
    else:
        print('>>> unknown type:')
        print(type(data))
        new = data
    return new


def xss_filter(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result.content = result.content
        try:
            jsondata = json.loads(result.content)
            result.content = json.dumps(jsonXssFilter(jsondata))
        except json.JSONDecodeError:
            result.content = jsonXssFilter(result.content)
        return result

    return wrapper
