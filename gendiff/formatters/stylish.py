REPLACER = ' '
REPLACE_COUNT = 4
OFFSET = 2
SIGNS = {
    'differ': '',
    'nested': '  ',
    'deleted': '- ',
    'added': '+ ',
    'unchanged': '  ',
    'changed': '- ',
    'changed_to': '+ ',
    'blanc': '  '
}


def make_indent(depth, sign):
    size = REPLACE_COUNT * depth - OFFSET
    padding = REPLACER * size
    return f'{padding}{sign}'


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


def node_processing(tree, depth=0):
    property = tree.get("key")
    children = tree.get('children')
    value = format_to_str(tree.get('value'), depth=depth)
    value_1 = format_to_str(tree.get('value_1'), depth=depth)
    value_2 = format_to_str(tree.get('value_2'), depth=depth)
    node_type = tree['type']
    indent = make_indent(depth, sign=SIGNS[node_type])

    if node_type == 'differ':
        lines = map(lambda node: node_processing(node, depth + 1), children)
        result = "\n".join(lines)
        return f'{{\n{result}\n}}'

    if node_type == 'nested':
        lines = map(lambda node: node_processing(node, depth + 1), children)
        result = "\n".join(lines)
        return f'{indent}{property}: {{\n{result}\n{indent}}}'

    if node_type in ('deleted', 'added', 'unchanged'):
        return f'{indent}{property}: {value}'

    if node_type == 'changed':
        string_1 = f'{indent}{property}: {value_1}'
        next_indent = make_indent(depth, sign=SIGNS['changed_to'])
        string_2 = f'{next_indent}{property}: {value_2}'
        return f'{string_1}\n{string_2}'

    raise ValueError('No such diff type name!')


def make_stylish(diff):
    return node_processing(diff)
