from gendiff.file_parcer import get_data
from gendiff.diff_structure import make_diff
from gendiff.formatters.stylish import make_stylish
from gendiff.formatters.plain import make_plain
from gendiff.formatters.json import make_json


def get_format(format_name):
    match format_name:
        case 'stylish' | None:
            return make_stylish
        case 'plain':
            return make_plain
        case 'json':
            return make_json
        case _:
            raise ValueError('No such format name!')


def generate_diff(file_path1, file_path2, format_name=None):
    data1 = get_data(file_path1)
    data2 = get_data(file_path2)
    diff = make_diff(data1, data2)
    format_diff = get_format(format_name)
    return format_diff(diff)
