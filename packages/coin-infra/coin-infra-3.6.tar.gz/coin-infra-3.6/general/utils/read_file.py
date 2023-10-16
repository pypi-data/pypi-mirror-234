import json


def read_json(path):
    with open(path, 'r') as jfile:
        data = json.load(jfile)
    return data
