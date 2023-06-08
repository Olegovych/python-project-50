import json
import yaml


def parse(data, file_format):
    if file_format == 'json':
        return json.loads(data)
    elif file_format in ('yml', 'yaml'):
        return yaml.safe_load(data)


def get_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    file_format = file_path.rpartition('.')[-1]
    return parse(data, file_format)
