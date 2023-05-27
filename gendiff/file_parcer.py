import json
import yaml


def parse(data, format_name):
    if format_name == 'json':
        return json.loads(data)
    elif format_name == 'yml' or format_name == 'yaml':
        return yaml.safe_load(data)


def get_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    format_name = file_path.rpartition('.')[-1]
    return parse(data, format_name)
