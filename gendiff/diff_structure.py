def make_diff(branch1, branch2):
    unique_keys = sorted(branch1.keys() | branch2.keys())
    diff = {}
    for key in unique_keys:
        if key not in branch1:
            diff[key] = {'added': branch2[key]}
        elif key not in branch2:
            diff[key] = {'deleted': branch1[key]}
        elif branch1[key] == branch2[key]:
            diff[key] = {'unchanged': branch1[key]}
        elif isinstance(branch1[key], dict) and isinstance(branch2[key], dict):
            diff[key] = {'nested': make_diff(branch1[key], branch2[key])}
        else:
            diff[key] = {'changed_from': branch1[key],
                         'changed_to': branch2[key]}
    return diff
