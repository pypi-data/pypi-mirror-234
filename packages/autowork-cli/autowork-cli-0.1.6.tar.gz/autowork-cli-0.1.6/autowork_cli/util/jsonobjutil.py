import json


def parse_to_obj(json_str, obj_class):
    parse_obj = json.loads(json_str)
    res = obj_class()
    res.__dict__ = parse_obj
    return res
