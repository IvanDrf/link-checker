from app.exc.internal import InternalError
from app.exc.external import ExternalError
from app.exc.file import FileError
from app.exc.user import UserError


def test_InternalError(message: str) -> None:
    default_message, error_message = get_message_from_errors(
        message, InternalError)

    assert default_message == 'Internal error'
    assert error_message == f'Internal error: {message}'


def test_ExternalError(message: str) -> None:
    default_message, error_message = get_message_from_errors(
        message, ExternalError)

    assert default_message == 'External error'
    assert error_message == f'External error: {message}'


def test_FileError(message: str) -> None:
    default_message, error_message = get_message_from_errors(
        message, FileError)

    assert default_message == 'File error'
    assert error_message == f'File error: {message}'


def test_UserError(message: str) -> None:
    default_message, error_message = get_message_from_errors(
        message, UserError)

    assert default_message == 'UserError: empty message'
    assert error_message == f'UserError: {message}'


def get_message_from_errors(message: str, Error: type[Exception]) -> tuple[str, str]:
    return raise_error(msg='', Error=Error), raise_error(msg=message, Error=Error)


def raise_error(msg: str, Error: type[Exception]) -> str:
    try:
        raise Error(msg)
    except Error as e:
        return e.__str__()
