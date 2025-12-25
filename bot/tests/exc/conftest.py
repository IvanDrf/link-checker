from pytest import fixture


@fixture
def message() -> str:
    return 'error message'
