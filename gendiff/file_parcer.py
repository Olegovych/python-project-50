import json
import yaml


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def get_data(path):
    str_data = read_file(path)
    ext = path.rpartition('.')[2]
    if ext == 'json':
        return json.loads(str_data)
    elif ext == 'yml' or ext == 'yaml':
        return yaml.safe_load(str_data)
