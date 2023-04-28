def format_to_plain(value):
    match value:
        case bool(val):
            return str(val).lower()
        case None:
            return 'null'
        case str(val):
            return f"'{val}'"
        case dict(val):
            return '[complex value]'
        case _:
            return str(value)


def make_lines(branch, path=''):
    lines = []
    for key, description in branch.items():
        key_path = f'{path}.{str(key)}' if path else str(key)
        description = list(description.items())
        key_status, value = description[0]
        if key_status != 'nested':
            value = format_to_plain(value)

        match key_status:
            case 'deleted':
                string_completion = "removed"
            case 'added':
                string_completion = f"added with value: {value}"
            case 'changed_from':
                _, new_value = description[1]
                new_value = format_to_plain(new_value)
                string_completion = f"updated. From {value} to {new_value}"
            case 'nested':
                nested_lines = make_lines(value, key_path)
                lines.extend(nested_lines)
                continue
            case _:
                continue

        lines.append(f"Property '{key_path}' was {string_completion}")
    return lines


def make_plain(diff):
    return '\n'.join(make_lines(diff))
