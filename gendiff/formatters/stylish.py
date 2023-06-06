REPLACER = ' '
SPACES_COUNT = 4
OFFSET = 2
SIGNS = {
    'differ': '',
    'added': '+ ',
    'deleted': '- ',
    'unchanged': '  ',
    'nested': '  ',
    'changed_from': '- ',
    'changed_to': '+ ',
    'blanc': '  '
}


def format_to_str(value, depth=0):
    match value:
        case bool(value):
            return str(value).lower()
        case None:
            return 'null'
        case dict(value):
            level_indent = make_indent(depth, sign=SIGNS['blanc'])
            nest_indent = make_indent(depth + 1, sign=SIGNS['blanc'])
            lines = map(
                lambda item:
                f'{nest_indent}{item[0]}: {format_to_str(item[1], depth + 1)}',
                value.items()
            )
            result = "\n".join(lines)
            return f'{{\n{result}\n{level_indent}}}'
        case _:
            return value


def make_indent(depth, sign):
    size = SPACES_COUNT * depth - OFFSET
    padding = REPLACER * size
    return f'{padding}{sign}' if depth else ''


def dict_processing(dict_, depth):
    lines = ['{']
    indent = make_indent(depth, sign=SIGNS['blanc'])
    for key, val in dict_.items():
        if isinstance(val, dict):
            value = dict_processing(val, depth + 1)
        else:
            value = format_to_str(val)
        lines.append(f'{indent}{key}: {value}')
    indent = make_indent(depth - 1, sign=SIGNS['blanc'])
    lines.append(indent + '}')
    return '\n'.join(lines)


def children_processing(tree, depth=0):
    property = tree.get("key")
    children = tree.get('children')
    value = format_to_str(tree.get('value'), depth=depth)
    value_1 = format_to_str(tree.get('value_1'), depth=depth)
    value_2 = format_to_str(tree.get('value_2'), depth=depth)
    node_type = tree['type']
    level_indent = make_indent(depth, sign=SIGNS['blanc'])
    type_indent = make_indent(depth, sign=SIGNS[node_type])

    if node_type == 'differ':
        lines = map(lambda node: children_processing(node, depth + 1), children)
        result = "\n".join(lines)
        return f'{{\n{result}\n}}'

    elif node_type == 'nested':
        lines = map(lambda node: children_processing(node, depth + 1), children)
        result = "\n".join(lines)
        return f'{type_indent}{property}: {{\n{result}\n{type_indent}}}'

    elif node_type == 'deleted':
        return f'{type_indent}{property}: {value}'

    elif node_type == 'added':
        return f'{type_indent}{property}: {value}'

    elif node_type == 'unchanged':
        return f'{type_indent}{property}: {value}'

    elif node_type == 'changed_from':
        return f'{type_indent}{property}: {value}'

    elif node_type == 'changed_to':
        return f'{type_indent}{property}: {value}'


def children_processing_old(children, depth):
    lines = ['{']
    for child in children:
        indent = make_indent(depth, sign=SIGNS[child['type']])
        property = child['key']
        if child['type'] == 'nested':
            value = children_processing(child['children'], depth + 1)
        else:
            value = format_to_str(child['value'], depth)
        lines.append(f'{indent}{property}: {value}')
    indent = make_indent(depth - 1, sign=SIGNS['blanc'])
    lines.append(indent + '}')
    return '\n'.join(lines)


def make_stylish(diff):
    return children_processing(diff)
