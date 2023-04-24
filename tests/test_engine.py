import pytest
from gendiff import generate_diff


@pytest.mark.parametrize(
    'file_path1,file_path2', [
        ('tests/fixtures/file1.json', 'tests/fixtures/file2.json'),
        ('tests/fixtures/plain1.yml', 'tests/fixtures/plain2.yaml')
    ]
)
def test_generate_diff_plain(file_path1, file_path2):
    difference = generate_diff(file_path1, file_path2)
    with open('tests/fixtures/plain_diff.txt') as diff_file:
        expected = diff_file.read()
    assert difference == expected
