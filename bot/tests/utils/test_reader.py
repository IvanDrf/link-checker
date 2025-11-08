from utils.file_reader import read_file
from tests.utils.fixture import files_paths


def test_reader(files_paths: tuple[str, ...]) -> None:
    files_data: tuple[str, ...] = ('<b>test</b>', '<code>test</code>')

    assert len(files_paths) == len(files_data)

    for i, file_path in enumerate(files_paths):
        res = read_file(file_path)

        assert isinstance(res, str)
        assert files_data[i] == res
