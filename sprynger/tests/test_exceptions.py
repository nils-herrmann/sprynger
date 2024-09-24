"""Module to test exceptions and warnings."""
import pytest

from sprynger import DocumentMetadata, Metadata, init
from sprynger.exceptions import AuthenticationError

def test_empty_response():
    """Test the empty response."""
    init()
    with pytest.warns(UserWarning, match='No results where found. Check the identifier.'):
        Metadata('does_not_exist', refresh=True)

def test_authentication_error():
    """Test the authentication error."""
    init(keys=['does_not_exist'])
    with pytest.raises(AuthenticationError, match='Authentication failed. Check your API key.'):
        DocumentMetadata('10.1007/s10660-023-09761-x', refresh=True)
