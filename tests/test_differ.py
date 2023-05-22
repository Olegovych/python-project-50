import pytest
import os.path
from gendiff import generate_diff


def get_path(file_name):
    return os.path.join(os.path.dirname(__file__), 'fixtures', file_name)


@pytest.mark.parametrize(
    'file_path1,file_path2', [
        (get_path('nested1.json'), get_path('nested2.json')),
        (get_path('nested1.yml'), get_path('nested2.yaml'))
    ]
)
@pytest.mark.parametrize(
    'diff_path,format_name', [
        (get_path('nested_diff.txt'), 'stylish'),
        (get_path('plain_diff.txt'), 'plain'),
        (get_path('json_diff.json'), 'json')
    ]
)
def test_generate_diff(file_path1, file_path2, diff_path, format_name):
    difference = generate_diff(file_path1, file_path2, format_name)
    with open(diff_path) as diff_file:
        expected = diff_file.read()
    assert difference == expected
