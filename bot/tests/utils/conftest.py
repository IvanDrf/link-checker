import pytest


@pytest.fixture
def files_paths() -> tuple[str, ...]:
    return ('tests/utils/test_1.html', 'tests/utils/test_2.html')
