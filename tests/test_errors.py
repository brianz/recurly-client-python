import pytest

from recurly.errors import UnauthorizedError
from recurly.errors import ValidationError


def test_error_printable():
    """Make sure __str__/__unicode__ works correctly in Python 2/3"""
    with pytest.raises(UnauthorizedError) as e:
        raise UnauthorizedError('recurly.API_KEY not set')

    assert 'recurly.API_KEY not set' in str(e)


def test_validationerror_printable():
    """Make sure __str__/__unicode__ works correctly in Python 2/3"""
    error = ValidationError.Suberror('field', 'symbol', 'message')
    suberrors = {'field': error}
    validation_error = ValidationError('')
    validation_error.__dict__['errors'] = suberrors
    assert str(validation_error) == 'symbol: field message'
