import itertools

REPLACER = ' '
SPACES_COUNT = 4
OFFSET = 2
SIGNS = {
    'added': '+ ',
    'deleted': '- ',
    'unchanged': '  ',
    'nested': '  ',
    'changed_from': '- ',
    'changet_to': '+ '
}


def format_to_str(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)


def make_stylish(branch, depth=1, is_child=True):
    def make_line():
        processed_value = make_stylish(value, depth + 1, is_child)
        lines.append(f'{indent}{sign}{key}: {processed_value}')

    if not isinstance(branch, dict):
        return format_to_str(branch)

    indent_size = SPACES_COUNT * depth - OFFSET
    indent = REPLACER * indent_size
    lines = []

    for key, description in branch.items():
        if not is_child:
            sign = REPLACER * OFFSET
            value = description
            make_line()
        else:
            for key_status, value in description.items():
                sign = SIGNS[key_status]
                is_child = True if key_status == 'nested' else False
                make_line()
                is_child = True
    last_indent = REPLACER * (SPACES_COUNT * (depth - 1))
    result = itertools.chain("{", lines, [last_indent + "}"])
    return '\n'.join(result)
