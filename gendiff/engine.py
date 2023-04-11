import json


def generate_diff(file_path1, file_path2):
    file_data1 = json.load(open(file_path1))
    file_data2 = json.load(open(file_path2))
    unique_keys = sorted(set(file_data1) | set(file_data2))
    difference = ['{']
    for key in unique_keys:
        if key in file_data1:
            if key in file_data2:
                val1, val2 = file_data1[key], file_data2[key]
                if val1 == val2:
                    difference.append(f'    {key}: {val1}')
                else:
                    difference.append(f'  - {key}: {val1}')
                    difference.append(f'  + {key}: {val2}')
            else:
                difference.append(f'  - {key}: {file_data1[key]}')
        else:
            difference.append(f'  + {key}: {file_data2[key]}')
    difference.append('}')
    return '\n'.join(difference)
