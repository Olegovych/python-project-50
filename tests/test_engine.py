from gendiff import generate_diff


# @pytest.mark.parametrize()
def test_generate_diff():
    file_path1 = 'tests/fixtures/file1.json'
    file_path2 = 'tests/fixtures/file2.json'
    difference = generate_diff(file_path1, file_path2)
    with open('tests/fixtures/plain_diff.txt') as diff_file:
        expected = diff_file.read()
    assert difference == expected
