import json
import yaml


def file_parcer(path):
    ext = path.rpartition('.')[2]
    if ext == 'json':
        return json.load(open(path))
    elif ext == 'yml' or ext == 'yaml':
        return yaml.safe_load(open(path))
