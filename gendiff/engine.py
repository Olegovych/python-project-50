from gendiff.file_parcer import file_parcer
from gendiff.formatters.stylish import make_stylish
from gendiff.formatters.plain import make_plain
from gendiff.formatters.json import make_json

FORMATTERS = {
    'stylish': make_stylish,
    'plain': make_plain,
    'json': make_json
}


def make_diff(branch1, branch2):
    unique_keys = sorted(branch1.keys() | branch2.keys())
    diff = {}
    for key in unique_keys:
        if key not in branch1:
            diff[key] = {'added': branch2[key]}
        elif key not in branch2:
            diff[key] = {'deleted': branch1[key]}
        elif branch1[key] == branch2[key]:
            diff[key] = {'unchanged': branch1[key]}
        elif isinstance(branch1[key], dict) and isinstance(branch2[key], dict):
            diff[key] = {'nested': make_diff(branch1[key], branch2[key])}
        else:
            diff[key] = {'changed_from': branch1[key],
                         'changet_to': branch2[key]}
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = file_parcer(file_path1)
    data2 = file_parcer(file_path2)
    diff = make_diff(data1, data2)
    format_diff = FORMATTERS.get(format_name, make_stylish)
    return format_diff(diff)
