from gendiff.formatters.stylish import format_to_str


def format_to_plain(value):
    match value:
        case dict(val):
            return '[complex value]'
        case str(val):
            return f"'{val}'"
        case _:
            return format_to_str(value)


def iter_children(children, path=''):
    lines = []
    children_iterator = iter(children)
    for child in children_iterator:
        key = child['key']
        property = f'{path}.{key}' if path else key

        type_ = child['type']
        if type_ == 'nested':
            nested_lines = iter_children(child['children'], property)
            lines.extend(nested_lines)
            continue

        value = format_to_plain(child['value'])
        if type_ == 'deleted':
            action = "removed"
        elif type_ == 'added':
            action = f"added with value: {value}"
        elif type_ == 'changed_from':
            child = next(children_iterator)
            new_value = format_to_plain(child['value'])
            action = f"updated. From {value} to {new_value}"
        else:
            continue

        lines.append(f"Property '{property}' was {action}")
    return lines


def make_plain(diff):
    return '\n'.join(iter_children(diff['children']))
