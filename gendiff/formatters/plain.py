from gendiff.formatters.stylish import format_to_str


def format_to_plain(value):
    match value:
        case dict(val):
            return '[complex value]'
        case str(val):
            return f"'{val}'"
        case _:
            return format_to_str(value)


def node_processing(tree, path=''):
    key = tree.get("key")
    property = f'{path}.{key}' if path else key
    children = tree.get('children')
    value = format_to_plain(tree.get('value'))
    value_1 = format_to_plain(tree.get('value_1'))
    value_2 = format_to_plain(tree.get('value_2'))
    node_type = tree['type']

    if node_type == 'differ':
        lines = (
            recurse for child in children
            if (recurse := node_processing(child))
        )
        return "\n".join(lines)

    if node_type == 'nested':
        lines = (
            recurse for child in children
            if (recurse := node_processing(child, property))
        )
        return "\n".join(lines)

    if node_type == 'deleted':
        return f"Property '{property}' was removed"

    if node_type == 'added':
        return f"Property '{property}' was added with value: {value}"

    if node_type == 'changed':
        return f"Property '{property}' was updated. From {value_1} to {value_2}"


def make_plain(diff):
    return node_processing(diff)
