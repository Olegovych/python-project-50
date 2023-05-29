REPLACER = ' '
SPACES_COUNT = 4
OFFSET = 2
SIGNS = {
    'added': '+ ',
    'deleted': '- ',
    'unchanged': '  ',
    'nested': '  ',
    'changed_from': '- ',
    'changed_to': '+ ',
    'blanc': '  '
}


def format_to_js_style(value):
    match value:
        case bool(val):
            return str(val).lower()
        case None:
            return 'null'
        case _:
            return value


def make_indent(depth, sign):
    size = SPACES_COUNT * depth - OFFSET
    blanc = REPLACER * size
    return f'{blanc}{sign}' if depth else ''


def dict_processing(dict_, depth):
    lines = ['{']
    indent = make_indent(depth, sign=SIGNS['blanc'])
    for key, val in dict_.items():
        if isinstance(val, dict):
            value = dict_processing(val, depth + 1)
        else:
            value = format_to_js_style(val)
        lines.append(f'{indent}{key}: {value}')
    indent = make_indent(depth - 1, sign=SIGNS['blanc'])
    lines.append(indent + '}')
    return '\n'.join(lines)


def children_processing(children, depth):
    lines = ['{']
    for child in children:
        indent = make_indent(depth, sign=SIGNS[child['type']])
        property = child['key']
        if child['type'] == 'nested':
            value = children_processing(child['children'], depth + 1)
        elif isinstance(child['value'], dict):
            value = dict_processing(child['value'], depth + 1)
        else:
            value = format_to_js_style(child['value'])
        lines.append(f'{indent}{property}: {value}')
    indent = make_indent(depth - 1, sign=SIGNS['blanc'])
    lines.append(indent + '}')
    return '\n'.join(lines)


def make_stylish(diff):
    return children_processing(diff['children'], depth=1)
