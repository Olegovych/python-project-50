import pytest
import os.path
from gendiff import generate_diff


@pytest.fixture
def get_path_fixture(request):
    file_name = request.param
    return os.path.join(os.path.dirname(__file__), 'fixtures', file_name)


file1 = file2 = diff = get_path_fixture


@pytest.mark.parametrize(
    'file1,file2', [
        ('nested1.json', 'nested2.json'),
        ('nested1.yml', 'nested2.yaml')
    ],
    indirect=True
)
@pytest.mark.parametrize(
    'diff,format_name', [
        ('stylish_diff.txt', 'stylish'),
        ('plain_diff.txt', 'plain'),
        ('json_diff.json', 'json')
    ],
    indirect=['diff']
)
def test_generate_diff(file1, file2, diff, format_name):
    difference = generate_diff(file1, file2, format_name)
    with open(diff) as diff_file:
        expected = diff_file.read()
    assert difference == expected


@pytest.mark.parametrize(
    'file1,file2,diff', [
        ('nested1.json', 'nested2.json', 'stylish_diff.txt')
    ],
    indirect=True
)
def test_default_format(file1, file2, diff):
    difference = generate_diff(file1, file2)
    with open(diff) as diff_file:
        expected = diff_file.read()
    assert difference == expected


@pytest.mark.parametrize(
    'file1,file2', [
        ('nested1.json', 'nested2.json')
    ],
    indirect=True
)
def test_raise_exception(file1, file2):
    with pytest.raises(ValueError):
        generate_diff(file1, file2, format_name="wrong")
