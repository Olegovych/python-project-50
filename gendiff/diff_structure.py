def make_children(data1, data2):
    keys = sorted(data1.keys() | data2.keys())
    children = []
    for key in keys:
        if key not in data1:
            children.append({
                'type': 'added',
                'key': key,
                'value': data2[key]
            })
        elif key not in data2:
            children.append({
                'type': 'deleted',
                'key': key,
                'value': data1[key]
            })
        elif data1[key] == data2[key]:
            children.append({
                'type': 'unchanged',
                'key': key,
                'value': data1[key]
            })
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            children.append({
                'type': 'nested',
                'key': key,
                'children': make_children(data1[key], data2[key])
            })
        else:
            children.append({
                'type': 'changed_from',
                'key': key,
                'value': data1[key]
            })
            children.append({
                'type': 'changed_to',
                'key': key,
                'value': data2[key]
            })
    return children


def make_diff(data1, data2):
    return {'type': 'differ', 'children': make_children(data1, data2)}
