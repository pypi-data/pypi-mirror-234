from copy import deepcopy


def convert(value, func):
    return func(value)


def get_value_from_dict(data: dict, key: str = None):
    value = deepcopy(data)
    if key:
        key_list = key.split(".")
        for k in key_list:
            if not isinstance(value, dict):
                break
            else:
                value = value.get(k)
    return value


def find_child(data, key="id", parent_key="parent_id"):
    result = []
    obj = {}
    for x in data:
        obj[x.get(key)] = x
    for x in data:
        parent_key_value = x.get(parent_key)
        parent = obj.get(parent_key_value, {})
        if parent:
            if not parent.get("children"):
                parent["children"] = []
            if not x.get("children"):
                x["children"] = []
            parent["children"].append(x)
        else:
            if not x.get("children"):
                x["children"] = []
            result.append(x)
    return result


def dict2list(data: dict, data_key="count", key_name="key", value_name="value"):
    result = []
    for key, value in data.items():
        if data_key:
            value = value.get(data_key)
        result.append({key_name: key, value_name: value})
    return result
