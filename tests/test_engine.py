import pytest
from gendiff import generate_diff


@pytest.mark.parametrize(
    'file_path1,file_path2', [
        ('tests/fixtures/file1.json', 'tests/fixtures/file2.json'),
        ('tests/fixtures/file1.yml', 'tests/fixtures/file2.yaml')
    ]
)
def test_generate_diff_flat(file_path1, file_path2):
    difference = generate_diff(file_path1, file_path2)
    with open('tests/fixtures/flat_diff.txt') as diff_file:
        expected = diff_file.read()
    assert difference == expected


@pytest.mark.parametrize(
    'file_path1,file_path2', [
        ('tests/fixtures/nested1.json', 'tests/fixtures/nested2.json'),
        ('tests/fixtures/nested1.yml', 'tests/fixtures/nested2.yaml')
    ]
)
def test_generate_diff_nested(file_path1, file_path2):
    difference = generate_diff(file_path1, file_path2)
    with open('tests/fixtures/nested_diff.txt') as diff_file:
        expected = diff_file.read()
    assert difference == expected


@pytest.mark.parametrize(
    'file_path1,file_path2', [
        ('tests/fixtures/nested1.json', 'tests/fixtures/nested2.json'),
        ('tests/fixtures/nested1.yml', 'tests/fixtures/nested2.yaml')
    ]
)
def test_generate_diff_plain(file_path1, file_path2):
    difference = generate_diff(file_path1, file_path2, format_name='plain')
    with open('tests/fixtures/plain_diff.txt') as diff_file:
        expected = diff_file.read()
    assert difference == expected
