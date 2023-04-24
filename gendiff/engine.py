import itertools
from gendiff.file_parcer import file_parcer


def make_line(prefix, key, value):
    if isinstance(value, bool):
        value = str(value).lower()
    return f'  {prefix} {key}: {value}'


def generate_diff(file_path1, file_path2):
    file_data1 = file_parcer(file_path1)
    file_data2 = file_parcer(file_path2)
    print(file_data1)
    print(file_data2)
    unique_keys = sorted(set(file_data1) | set(file_data2))
    difference = []
    for key in unique_keys:
        if key in file_data1:
            val1 = file_data1[key]
            if key in file_data2:
                val2 = file_data2[key]
                if val1 == val2:
                    difference.append((' ', key, val1))
                else:
                    difference.append(('-', key, val1))
                    difference.append(('+', key, val2))
            else:
                difference.append(('-', key, val1))
        else:
            val2 = file_data2[key]
            difference.append(('+', key, val2))
    lines = itertools.starmap(make_line, difference)
    result = itertools.chain("{", lines, "}")
    return '\n'.join(result)
